#coding=utf-8
# Create your views here.
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
from core.models import *

from tools.const import  StatusUser, StatusUnit, IsAdmin, IsApplicant, IsExpert, IsSysAdmin, ApproveStatus, StatusApprove, ProjectStatus
from tools.decorator import Ajax, Users, Auth, dumps
from tools.helper import CallBack, ErrCallBack, CurPage, StartLimit, IdArray, GetParam,\
FillModel, Items, Str2DateTime, TryGetParam, GetArrayParams, RawDoc, OK, WriteDictToExcel, ExcelRender
#############################################
#公共模块
#############################################
def login(request):
	name = request.POST.get('name')
	pwd = request.POST.get('password')
	code = request.POST.get('code')
	if request.session['verify'] != code:
		return render_to_response('login/login.htm',{
			'errormessage': '验证码错误！'
		})
	if not name or not pwd:
		return render_to_response('login/login.htm',{
			'errormessage': '用户名密码不能为空！'
		})
	user = User.objects.filter(name=name, password=pwd, status=StatusUser.NORMAL)
	if not user:
		return render_to_response('login/login.htm',{
			'errormessage': '用户名或密码错误！'
		})
	else:
		user= user[0]
		request.session[Const.User] =user
		types = ''
		for p in ProjectType.objects.all().values('pk', 'name'):
			if types: types += ';'
			types += str(p['pk']) + ',' + p['name']

		user.login_count+=1
		user.last_activity_ip=user.get_client_ip(request)

		user.save()
		return render_to_response('main.html', {'user': user, 'project_types': types})


@Ajax
def register_user(request):
	"""
	注册项目申请人
	"""
	register_user_values = ('name', 'password', 'real_name', 'unit_id', 'sex', 'phone', 'mobile', 'remark')
	kv = GetParam(request, *register_user_values)
	u = User()
	FillModel(kv, u)

	u.role = Role.objects.filter(code=Const.APPLICANT)[0]
	u.status = StatusUser.APPROVE
	u.save()
	return CallBack('用户注册信息已提交，等待管理员审核！')


@Ajax
def register_unit(request):
	register_unit_values = ('name', 'address', 'parent_unit_id', 'phone')
	kv = GetParam(request, *register_unit_values)
	u = Unit()
	FillModel(kv, u)
	u.status = StatusUnit.APPROVE
	u.save()
	return CallBack('单位注册信息已提交，等待管理员审核！')


def main(request):
	Auth(request)
	user = request.session[Const.User]
	types = ''
	for p in ProjectType.objects.all().values('pk', 'name'):
		if types: types += ';'
		types += str(p['pk']) + ',' + p['name']
	return render_to_response('main.html', {'user': user, 'project_types': types})

#############################################
#用户管理
#############################################
@Ajax
def user_list(request):
	user_list_values = (
	'pk', 'name', 'real_name', 'unit__name', 'unit__level', 'unit__parent_unit__name', 'role__name')
	start, limit = StartLimit(request)
	user = Auth(request, Const.ADMIN)
	if not user: raise Http404

	if IsSysAdmin(user):
		items = User.objects.filter(
			status=StatusUser.NORMAL,
		).order_by('unit__level').values(*user_list_values)[start:limit]
		total = User.objects.filter(
			status=StatusUser.NORMAL,
		).count()
		return CurPage(total, items)

	else:
		items = User.objects.filter(
			~(Q(role__code=Const.ADMIN)&Q(unit_id=user.unit_id)),#无法修改本单位管理员
			Q(status=StatusUser.NORMAL),
			Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id)
		).order_by('unit__level').values(*user_list_values)[start:limit]
		total = User.objects.filter(
			Q(status=StatusUser.NORMAL),
			Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id)
		).count()
		return CurPage(total, items)


@Ajax
def expert_set(request):
	Auth(request)
	kv = GetParam(request, 'ids', 'expert_ids')
	experts = User.objects.filter(id__in=IdArray(kv['expert_ids']))
	projectapplys=ProjectApply.objects.filter(id__in=IdArray(kv['ids']))
	for p in projectapplys:
		for e in experts:
			pe=ProjectApplyExpert()
			pe.expert=e
			pe.apply=p
			pe.save()
		p.status=StatusApprove.WAIT_EXPERT
		p.save()
	return CallBack('设置成功，等待专家审核！')


@Ajax
def user_name(request):
	kv = GetParam(request, 'name')
	if User.objects.filter(name=kv['name']).exists():
		return CallBack(Const.FAIL)
	else:
		return CallBack(Const.OK)



@Ajax
def user_list_approve(request):
	user_list_approve_values = (
	'pk', 'name', 'real_name', 'unit__name', 'unit__level', 'unit__parent_unit__name', 'regtime')
	start, limit = StartLimit(request)
	user = Auth(request, Const.ADMIN)
	if not user: raise Http404
	if IsSysAdmin(user):
		items = User.objects.filter(
			status=StatusUser.APPROVE,
		).order_by('unit__level').values(*user_list_approve_values)[start:limit]
		total = User.objects.filter(
			status=StatusUser.APPROVE,
		).count()
		return CurPage(total, items)
	else:
		items = User.objects.filter(
			Q(status=StatusUser.APPROVE),
			Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id)
		).order_by('unit__level').values(*user_list_approve_values)[start:limit]
		total = User.objects.filter(
			Q(status=StatusUser.APPROVE),
			Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id)
		).count()
		return CurPage(total, items)


@Ajax
def user_del(request):
	kv = GetParam(request, 'ids')
	if Auth(request, Const.ADMIN):
		User.objects.filter(id__in=IdArray(kv['ids'])).delete()
	else:
		raise Http404


@Ajax
def user_add(request):
	user_add_values = ('name', 'password', 'real_name', 'unit_id', 'role_id', 'sex', 'phone', 'mobile', 'remark','study_type_name')
	kv = GetParam(request, *user_add_values)
	u = User()
	FillModel(kv, u)

	u.save()
	return CallBack(Const.OK)


@Ajax
def user_self_update(request):
	user_self_update_values=('real_name','email','password','sex','phone','mobile')
	cur_user=Auth(request)
	kv = GetParam(request, *user_self_update_values)
	u = User.objects.get(pk=cur_user.pk)
	FillModel(kv, u)
	u.save()
	return CallBack("保存成功！")



@Ajax
def user_update(request):
	user_update_values = ('pk', 'name', 'password','email',
	                      'real_name', 'unit_id', 'role_id'
	                      , 'sex', 'phone', 'mobile', 'remark','study_type_name')

	kv = GetParam(request, *user_update_values)
	u = User.objects.get(pk=int(kv['pk']))
	FillModel(kv, u)

	u.save()
	print 'ok'
	return CallBack(Const.OK)


@Ajax
def user_detail(request):
	kv = GetParam(request, 'id')
	user_update_values = ('pk', 'name', 'password','email',
	                      'real_name', 'unit_id', 'role_id','study_type_name',
	                      'sex', 'phone', 'mobile', 'remark')

	return User.objects.filter(pk=int(kv['id'])).values(*user_update_values)[0]


def user_show_detail(request):
	kv = GetParam(request, 'pk')
	obj = User.objects.get(pk=int(kv['pk']))
	return render_to_response('user_details.html', {'obj': obj})


@Ajax
def user_approve(request):
	Auth(request, Const.ADMIN)
	kv = GetParam(request, 'ids', 'pass', 'option')
	success=bool(kv['pass'] == 'true')
	use_status = StatusUser.NORMAL if success\
	else StatusUser.APPROVE_FAIL
	User.objects.filter(id__in=IdArray(request.POST.get('ids'))).update(status=use_status)
	return CallBack(Const.OK)


#############################################
#combo
#############################################
@Ajax
def unit_combo(request):
	user=Auth(request,Const.ADMIN)
	unit_combo_values = ('pk', 'name')
	filters=[Q(status=StatusUnit.NORMAL)]
	if not IsSysAdmin(user):
		filters.append(Q(pk=user.unit_id)|Q(parent_unit_id=user.unit_id))
	items = Unit.objects.filter(*filters).order_by('level').values(*unit_combo_values)
	return Items(items)


@Ajax
def role_combo(request):
	user=Auth(request,Const.ADMIN)
	filter=[]
	if user.unit.level==2:
		filter.append(~Q(code=Const.EXPERT))
		filter.append(~Q(code=Const.ADMIN))
	elif user.unit.level==1:
		filter.append(~Q(code=Const.EXPERT))
	items = Role.objects.filter(*filter).order_by('level').values('pk', 'name')
	return Items(items)


@Ajax
def projecttype_combo(request):
	user=Auth(request)
	if IsApplicant(user) and user.unit_id!=3:
		types=UnitLimitProjectType.objects.filter(
			unit_id=user.unit_id
		).values('project_type__pk','project_type__name')
		return  Items(types)
	else:
		projecttype_combo_values = ('pk', 'name')
		items = ProjectType.objects.all().values(*projecttype_combo_values)
		return  Items(items)


@Ajax
def expert_combo(request):
	Auth(request,Const.ADMIN)
	kv=GetParam(request,'type')

	expert_combo_values = ('pk', 'name')
	items = User.objects.filter(role__code=Const.EXPERT,study_type_name=kv['type']).values(*expert_combo_values)
	return  Items(items)

#############################################
#单位管理管理
#############################################
@Ajax
def unit_list(request):
	unit_list_values = ('pk', 'name', 'parent_unit__name',
	                    'max_project', 'apply_starttime', 'apply_endtime', 'address', 'level','no')
	start, limit = StartLimit(request)
	user = Auth(request, Const.ADMIN)
	if user:
		condition=[Q(status=StatusUnit.NORMAL),
		           Q(level__gte=user.unit.level),~Q(parent_unit__id=0)]

		items = Unit.objects.filter(
			*condition
		).order_by('level').values(*unit_list_values)[start:limit]
		total = Unit.objects.filter(
			*condition).count()
		return CurPage(total, items)
	else:
		raise Http404


@Ajax
def unit_list_approve(request):
	unit_list_approve_values = ('pk', 'name', 'parent_unit__name',
	                            'project_type__name', 'address', 'level', 'regtime')
	start, limit = StartLimit(request)
	user = Auth(request, Const.ADMIN)
	if user:
		items = Unit.objects.filter(
			status=StatusUnit.APPROVE,
			level__gte=user.unit.level
		).order_by('level').values(*unit_list_approve_values)[start:limit]
		total = Unit.objects.filter(status=StatusUnit.APPROVE).count()
		return CurPage(total, items)
	else:
		raise Http404


@Ajax
def unit_add(request):
	unit_add_values = ('name', 'parent_unit_id', 'project_type_id',
	                   'max_project', 'address', 'phone','no')
	kv = GetParam(request, *unit_add_values)
	user = Auth(request, Const.ADMIN)
	if user:
		@transaction.commit_on_success
		def runTran():
			ut = Unit()
			FillModel(kv, ut,exclude=['project_type_id'])
			project_types=request.POST.getlist('project_type_id')
			ut.save()
			for p in project_types:
				ul=UnitLimitProjectType()
				ul.project_type_id=int(p)
				ul.unit_id=ut.id
				ul.save()
		runTran()
		return CallBack(Const.OK)
	else:
		raise Http404


@Ajax
def unit_update(request):
	if not Auth(request, Const.ADMIN):raise Http404

	unit_update_values = ('pk', 'name', 'parent_unit_id', 'project_type_id', 'address',
	                      'max_project', 'apply_starttime', 'apply_endtime','no')
	kv = GetParam(request, *unit_update_values)
	@transaction.commit_on_success
	def runTran():
		u = Unit.objects.get(pk=int(kv['pk']))
		FillModel(kv, u,exclude=['project_type_id'])
		UnitLimitProjectType.objects.filter(unit_id=u.id).delete()
		uls=request.POST.getlist('project_type_id')
		for pk in uls:
			ul=UnitLimitProjectType()
			ul.project_type_id=int(pk)
			ul.unit_id=u.id
			ul.save()
		u.save()
	runTran()
	return CallBack(Const.OK)


@Ajax
def unit_details(request):
	unit_details_values = ('pk', 'name', 'parent_unit_id', 'address', 'phone',
	                       'max_project', 'apply_starttime', 'apply_endtime','no')
	kv = GetParam(request, 'id')

	obj= Unit.objects.filter(pk=int(kv['id'])).values(*unit_details_values)[0]

	ptypes= UnitLimitProjectType.objects.filter(unit_id=int(kv['id'])).\
	values('project_type__pk')
	ptypes_array=[]
	for p in ptypes:
		ptypes_array.append(str(p['project_type__pk']))
	obj['project_type_id']=','.join(ptypes_array)
	return obj
@Ajax
def unit_del(request):
	kv = GetParam(request, 'ids')
	if Auth(request, Const.ADMIN):
		Unit.objects.filter(id__in=IdArray(kv['ids'])).delete()
	else:
		raise Http404


@Ajax
def unit_approve(request):
	kv = GetParam(request, 'ids', 'pass', 'option')
	if Auth(request, Const.ADMIN):
		success=bool(kv['pass'] == 'true')
		unit_status = StatusUnit.NORMAL if success else StatusUnit.APPROVE_FAIL
		Unit.objects.filter(id__in=IdArray(request.POST.get('ids'))).update(status=unit_status)
	else:
		raise Http404


#############################################
#项目管理
#############################################
@Ajax
def project_list(request):
	project_list_values = (
	'pk', 'name', 'no',
	'applicant_time',  'ptype__name','comple_time')
	start, limit = StartLimit(request)
	user = Auth(request, Const.ADMIN, Const.APPLICANT)
	if not user: raise Http404
	conditions = []
	projecttype = TryGetParam(request, 'projecttype')
	if projecttype: conditions.append(Q(ptype_id=int(projecttype.value)))
	if IsAdmin(user):
		if not IsSysAdmin(user):
			conditions.append(Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
		items = Project.objects.filter(*conditions).values(*project_list_values)[start:limit]
		total = Project.objects.filter(*conditions).count()
		return CurPage(total, items)

	if IsApplicant(user):
		if TryGetParam(request, 'iscombo'):
			status = TryGetParam(request, 'status')
			if not status: raise Http404

			return Project.objects.filter(
				applicant_id=user.id,
				status=int(status.value)).values(*project_list_values)
		else:
			q = Q(applicant_id=user.id)
			projecttype = TryGetParam(request, 'projecttype')
			if projecttype:
				q &= Q(ptype_id=int(projecttype.value))
			items = Project.objects.filter(q).values(*project_list_values)[start:limit]
			total = Project.objects.filter(q).count()
			return CurPage(total, items)

	else:
		raise Http404


@Ajax
def project_search(request):
	user = Auth(request, Const.ADMIN)
	start, limit = StartLimit(request)
	status=TryGetParam(request,'status')
	status=int(status.value)
	conditions = []
	if not IsSysAdmin(user):
		conditions.append(Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
	key = TryGetParam(request, 'key')
	value=TryGetParam(request,'value')
	if key:
		if key.value == 'name' and key.value!='':
			if status!=3:
				conditions.append(Q(name__contains=value.value))
			else:
				conditions.append(Q(project_name__contains=value.value))

		elif key.value == 'applicant__name' and key.value!='':
			conditions.append(Q(applicant__name=value.value))
		elif key.value == 'applicant_time':
			start_time=TryGetParam(request,'start_time')
			end_time=TryGetParam(request,'end_time')
			start_time_val= start_time.value.replace('年','-').replace('月','-').replace('日','')
			end_time_val=end_time.value.replace('年','-').replace('月','-').replace('日','')
			conditions.append(Q(applicant_time__range=[start_time_val,end_time_val]))
		elif key.value == 'unit__name' and key.value!='':
			conditions.append(Q(unit__name=value.value))

	if status==3:#待审核
		conditions.append(Q(status__in=(
			StatusApprove.WAIT_ADMIN_0,
			StatusApprove.WAIT_ADMIN_1,
			StatusApprove.WAIT_ADMIN_2
		)))
		items = ProjectApply.objects.filter(*conditions).values(
			'pk', 'project_name', 'project_no', 'status','applicant_time',
			'unit__name', 'unit__level', 'project_type__name')[start:limit]
		for f in items:
			f['name']=f['project_name']
			f['ptype__name']=f['project_type__name']
			f['no']=f['project_no']
		total = ProjectApply.objects.filter(*conditions).count()
		return CurPage(total, items)

	elif status==4:#待变更
		result=ProjectExChange.objects.filter(status__in=(
			StatusApprove.WAIT_ADMIN_0,
			StatusApprove.WAIT_ADMIN_1,
			StatusApprove.WAIT_ADMIN_2
		)).values('project_id')
		pks=[f['project_id'] for f in  result]

		conditions.append(Q(id__in=pks))

	elif status==5:#待结项
		result=ProjectEndApply.objects.filter(status__in=(
			StatusApprove.WAIT_ADMIN_0,
			StatusApprove.WAIT_ADMIN_1,
			StatusApprove.WAIT_ADMIN_2
		)).values_list('project_id')
		pks=[f['project_id'] for f in result]
		conditions.append(Q(id__in=pks))

	elif status<2:
		conditions.append(Q(status=status))

	items = Project.objects.filter(*conditions).values('pk', 'name', 'no', 'status',
		'applicant_time', 'unit__name', 'unit__level', 'ptype__name')[start:limit]
	total = Project.objects.filter(*conditions).count()
	return CurPage(total, items)


@Ajax
def project_count(request):
	key = TryGetParam(request, 'key')
	value=TryGetParam(request,'value')
	start_time=TryGetParam(request,'start_time')
	end_time=TryGetParam(request,'end_time')
	start_time_val= start_time.value.replace('年','-').replace('月','-').replace('日','')
	end_time_val=end_time.value.replace('年','-').replace('月','-').replace('日','')
	normal=Q(status=StatusProject.NORMAL)
	lazy=Q(status=StatusProject.NORMAL)
	postback=Q(status=StatusProject.BACK)
	undo=Q(status=StatusProject.UNDO)
	if key:
		if key.value == 'name' and key.value!='':
			normal&=(Q(name__contains=value.value))
		elif key.value == 'applicant__name' and key.value!='':
			lazy&=Q(applicant__name=value.value)
		elif key.value == 'applicant_time':
			postback&=Q(applicant_time__range=[start_time_val,end_time_val])
		elif key.value == 'unit__name' and key.value!='':
			undo&=Q(unit__name=value.value)
	return {
		'normal':Project.objects.filter(normal).all().count(),
	        'lazy':Project.objects.filter(lazy).all().count(),
	        'postback':Project.objects.filter(postback).all().count(),
		'undo':Project.objects.filter(undo).all().count()
	}


@Ajax
def project_type_list(request):

	project_type_list_values = ('pk', 'name', 'waring_day','allow_apply','max_project_num')
	start, limit = StartLimit(request)
	user = Auth(request, Const.ADMIN)
	if user:
		items = ProjectType.objects.all().values(*project_type_list_values)[start:limit]
		total = ProjectType.objects.all().count()

		return CurPage(total, items)
	else:
		raise Http404


@Ajax
def project_exchange_add(request):
	project_exchange_add = ('applicant_opinion', 'forward_status', 'pk','project_exchage_add_date')
	kv = GetParam(request, *project_exchange_add)
	user = Auth(request, Const.APPLICANT)
	if not user:raise Http404
	if user:
		p = ProjectExChange()
		p.applicant_id = user.pk
		project_apply = ProjectApply.objects.get(pk=kv['pk'])
		project=project_apply.GetProject()
		if not project:
			return CallBack('需要立项后才能进行改操作！')
		p.project = project
		p.unit_id = user.unit_id
		p.applicant_opinion = kv['applicant_opinion']
		p.forward_status = kv['forward_status']
		if int(p.forward_status)==StatusProject.LAZY:
			p.new_project_end_date=Str2DateTime(kv['project_exchage_add_date'])
		p.status = StatusApprove.WAIT_ADMIN_2
		p.save()
		return CallBack('您的项目变更申请已经提交,<br/>请等待管理员审核！')
	else:
		raise Http404

@Ajax
def project_rollback_add(request):
	kv = GetParam(request,'applicant_opinion',  'pk')
	user = Auth(request, Const.APPLICANT)
	if user:
		p = ProjectRollbackApply()
		p.applicant_id = user.pk
		porject_apply = ProjectApply.objects.get(pk=int(kv['pk']))
		if porject_apply.status!=StatusApprove.WAIT_ADMIN_2 \
		and porject_apply.status!=StatusApprove.WAIT_ADMIN_1:
			return CallBack("无法对该项目执行退回操作!")

		applys= ProjectRollbackApply.objects.filter(project_apply_id=int(kv['pk']))
		for a in applys:
			if a.status in (StatusApprove.WAIT_ADMIN_0,
			                StatusApprove.WAIT_ADMIN_1,
			                StatusApprove.WAIT_ADMIN_2):
				return CallBack('必等待审核完毕才能再次提交！')

		p.project_apply = porject_apply
		p.unit_id = user.unit_id
		p.applicant_opinion = kv['applicant_opinion']
		p.status = StatusApprove.WAIT_ADMIN_2
		p.save()
		return CallBack('您的项目变退回请已经提交,<br/>请等待管理员审核!')
	else:
		raise Http404

@Ajax
def project_rollback_approve(request):
	def ProceedApprove(user, success):
		if IsAdmin(user):
			if user.unit.level == 1:
				#一级单位查看 子部门 待审核
				return StatusApprove.SUCCESS if success else StatusApprove.FAILED_ADMIN_1
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				return StatusApprove.WAIT_ADMIN_1 if success else StatusApprove.FAILED_ADMIN_2
	user = Auth(request, Const.ADMIN)
	if user:
		kv = GetParam(request, 'ids', 'pass', 'option')
		success =bool(kv['pass'] == 'true')

		approve_status = ProceedApprove(user, success)
		bulk, now, idArr = [], datetime.now(), IdArray(kv['ids'])
		ProjectRollbackApply.objects.filter(id__in=idArr).update(status=approve_status)
		rollbacks = ProjectRollbackApply.objects.filter(id__in=idArr)

		bulk = [ProjectRollbackApplyApprove(
			approve=user,
			approvetime=now,
			details=p,
			approve_opinion=kv['option'],
			success=success) for p in rollbacks]
		ProjectRollbackApplyApprove.objects.bulk_create(bulk)

		#项目退回申请通过
		if approve_status == StatusApprove.SUCCESS:
			for p in rollbacks:
				p.project_apply.status=StatusApprove.WAIT_SUBMIT
				p.project_apply.save()
		return CallBack('审核成功！' + ApproveStatus.get(approve_status))
	else:
		raise Http404


@Ajax
def project_rollback_list(request):
	def ProejctRollbackList(user):
		if IsAdmin(user):
			if user.unit.level == 0:
				#科技局查看 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_0)
			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_1)\
				& (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_2)&Q(unit_id=user.unit.id)
		elif IsApplicant(user):
			#项目申请人
			return Q(applicant_id=user.pk)
		raise Http404

	user = Auth(request, Const.APPLICANT, Const.ADMIN)
	start, limit = StartLimit(request)
	user_filert = ProejctRollbackList(user)
	items =ProjectRollbackApply.objects.filter(user_filert).values('pk',
		'project_name', 'project_type__name', 'project_no',
		'applicant_time', 'status', 'project_status','applicant_opinion')[start:limit]
	total = ProjectRollbackApply.objects.filter(user_filert).count()
	return CurPage(total, items)



@Ajax
def project_end_add(request):
	user = Auth(request, Const.APPLICANT)
	if not user:raise Http404
	kv, group_kv=GetArrayParams(request,
		'final_achieve_name',
		'main_user_name',
		'achive_fomat',
		'study_type_name',
		'plain_end_time',
		'real_end_time',
		'font_num',
		'unit_and_time',
		'go_where',
		'final_desc',
		'project_apply_id',
		'mingwei_option',
		'g__achieves__name',
		'g__achieves__unit_and_time',
		'g__achieves__desc',
		'file_code')

	ap=ProjectApply.objects.get(pk= int(kv['project_apply_id']))
	project=ap.GetProject()
	if not ap:return CallBack('必须立项的项目才可进该操作')

	@transaction.commit_on_success
	def runTran():
		u=ProjectEndApply()
		FillModel(kv, u,exclude='project_apply_id')
		u.project=project
		u.applicant_id=user.pk
		u.unit_id=user.unit_id
		u.status=StatusApprove.WAIT_ADMIN_2
		u.save()

		achieves = group_kv['achieves'].values()
		for a in achieves:
			pnaa=ProjectEndApplyApplicantAchieve()
			FillModel(a,pnaa,exclude=['file_code'])
			pnaa.end_apply_id=u.pk
			pnaa.save()
		d = Document()

		filecode=kv['file_code']
		d.doc = RawDoc(filecode)
		assert d.doc

		d.pdf = Const.HERE + '/media/project/' + filecode + '.pdf'
		d.project_no = filecode
		d.save()
		t = ConvertPDFTask()
		t.documentid = int(d.pk)
		t.save()
		u.document_id=d.pk
		u.save()

	runTran()
	return OK



#todo unit
@Ajax
def project_end_approve(request):
	def ProceedApprove(user, success):
		if IsAdmin(user):
			if user.unit.level==0:
				return StatusApprove.SUCCESS if success else StatusApprove.FAILED_ADMIN_0
			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				return StatusApprove.WAIT_ADMIN_0 if success else StatusApprove.FAILED_ADMIN_1
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				return StatusApprove.WAIT_ADMIN_1 if success else StatusApprove.FAILED_ADMIN_1

	user = Auth(request, Const.ADMIN)
	if user:
		kv = GetParam(request, 'ids', 'pass', 'option')
		success =bool(kv['pass'] == 'true')
		approve_status = ProceedApprove(user, success)
		bulk, now, idArr = [], datetime.now(), IdArray(kv['ids'])
		ProjectEndApply.objects.filter(id__in=idArr).update(status=approve_status)
		ends = ProjectEndApply.objects.filter(id__in=idArr)

		bulk = [ProjectEndApplyApprove(
			approve=user,
			approvetime=now,
			details=p,
			approve_opinion=kv['option'],
			success=success) for p in ends]
		ProjectEndApplyApprove.objects.bulk_create(bulk)

		#项目退回申请通过
		if approve_status == StatusApprove.SUCCESS:
			for p in ends:
				p.project.status=StatusProject.DONE
				p.project.save()
		return CallBack('审核成功！' + ApproveStatus.get(approve_status))
	else:
		raise Http404


@Ajax
def project_end_list(request):
	def ProejctEndList(user):
		if IsAdmin(user):
			if user.unit.level == 0:
				#科技局查看 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_0)
			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_1)\
				& (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_2)&Q(unit_id=user.unit.id)
		elif IsApplicant(user):
			#项目申请人
			return Q(applicant_id=user.pk)
		raise Http404
	project_end_list = ('pk', 'final_achieve_name', 'main_user_name', 'plain_end_time','project__no','document_id',
	                         'real_end_time', 'status')
	user = Auth(request, Const.APPLICANT, Const.ADMIN)
	start, limit = StartLimit(request)
	user_filert = ProejctEndList(user)
	items =ProjectEndApply.objects.filter(user_filert).values(*project_end_list)[start:limit]
	total = ProjectEndApply.objects.filter(user_filert).count()
	return CurPage(total, items)


@Ajax
def project_exchange_list(request):
	def ProejctExchangeList(user):
		if IsAdmin(user):
			if user.unit.level == 0:
				#科技局查看 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_0)
			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_1)\
				& (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				return Q(status=StatusApprove.WAIT_ADMIN_2)&Q(unit_id=user.unit.id)

		elif IsApplicant(user):
			#项目申请人
			return Q(applicant_id=user.pk)
		raise Http404

	project_exchange_list = ('pk', 'project_name', 'project_type__name', 'project_no',
	                         'applicant_time', 'status', 'forward_status', 'project_status','applicant_opinion')
	user = Auth(request, Const.APPLICANT, Const.ADMIN)
	start, limit = StartLimit(request)
	user_filert = ProejctExchangeList(user)
	items = ProjectExChange.objects.filter(user_filert).values(*project_exchange_list)[start:limit]
	total = ProjectExChange.objects.filter(user_filert).count()
	return CurPage(total, items)




def project_show_details(request):
	Auth(request)
	kv = GetParam(request, 'pk')
	pk = kv['pk']
	print 'pk is'+str(pk)
	project = Project.objects.get(pk=int(pk))
	return render_to_response('project_details.html', {'obj': project})


def project_apply_show_details(request):
	Auth(request)
	kv = GetParam(request, 'pk')
	pk = kv['pk']
	apply = ProjectApply.objects.get(pk=int(pk))
	proejct=apply.GetProject()
	apply.project_status='未立项' if not proejct else ProjectStatus.get(proejct.status)
	return render_to_response('project_apply_details.html', {'obj': apply})

@Ajax
def admin_notify_count(request):
	user=Auth(request,Const.ADMIN)
	def ProjectApplyCount(admin_ask_expert):
		if user.unit.level == 0:
			#科技局查看 待审核
			if admin_ask_expert:
				q = Q(status=StatusApprove.WAIT_SET_EXPERT)
			else:
				q = Q(status=StatusApprove.WAIT_ADMIN_0)
		elif user.unit.level == 1:
			#一级单位查看 子部门 待审核
			q = Q(status=StatusApprove.WAIT_ADMIN_1) & (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
		elif user.unit.level == 2:
			#二级单位管理员 待审核
			q = Q(status=StatusApprove.WAIT_ADMIN_2) & Q(unit_id=user.unit_id)
		else:
			raise Http404
		return ProjectApply.objects.filter(q).count()

	def ProejctExchangeCount():

		if user.unit.level == 0:
			#科技局查看 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_0)
		elif user.unit.level == 1:
			#一级单位查看 子部门 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_1)\
			& (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
		elif user.unit.level == 2:
			#二级单位管理员 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_2)&Q(unit_id=user.unit.id)
		else:
			raise Http404
		return ProjectExChange.objects.filter(q).count()

	def ProjectEndCount():
		if user.unit.level == 0:
			#科技局查看 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_0)
		elif user.unit.level == 1:
			#一级单位查看 子部门 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_1)\
			& (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
		elif user.unit.level == 2:
			#二级单位管理员 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_2)&Q(unit_id=user.unit.id)
		else:
			raise Http404
		return ProjectEndApply.objects.filter(q).count()

	def ProjectBackCount():
		if user.unit.level == 0:
		#科技局查看 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_0)
		elif user.unit.level == 1:
			#一级单位查看 子部门 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_1)\
			& (Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
		elif user.unit.level == 2:
			#二级单位管理员 待审核
			q= Q(status=StatusApprove.WAIT_ADMIN_2)&Q(unit_id=user.unit.id)
		else:
			raise Http404
		return ProjectRollbackApply.objects.filter(q).count()

	result={}
	if user.unit.level == 0:
		result['apply_ask_expert']=ProjectApplyCount(True)
	result['apply']=ProjectApplyCount(False)
	result['back']=ProjectBackCount()
	result['end']=ProjectEndCount()
	result['exchange']=ProejctExchangeCount()
	return result

@Ajax
def project_apply_list(request):
	def ProjectApplyList(request):
		user = Auth(request)
		if IsAdmin(user):
			if user.unit.level == 0:
				#等待专家评审
				if TryGetParam(request, 'admin_ask_expert'):
					q = Q(status=StatusApprove.WAIT_SET_EXPERT)
				#等待民委审查
				elif TryGetParam(request,'wait_admin_look'):
					q = Q(status=StatusApprove.WAIT_AMIDN_0_LOOK)
				else:
					q = Q(status=StatusApprove.WAIT_ADMIN_0)
				r=TryGetParam(request,'study_type_name')
				if r:
					q&=Q(study_type_name=str(r.value))
			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				q = Q(status=StatusApprove.WAIT_ADMIN_1) & (
				Q(unit__parent_unit_id=user.unit.id) | Q(unit_id=user.unit.id))
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				q = Q(status=StatusApprove.WAIT_ADMIN_2) & Q(unit_id=user.unit_id)
			else:
				raise Http404
			r = TryGetParam(request, 'projecttype')
			if r and int(r.value) != 0:

				q &= Q(project_type__id=int(r.value))
			return q
		elif IsApplicant(user):
			#项目申请人
			q = Q(applicant_id=user.pk)
			r = TryGetParam(request, 'projecttype')
			if r and int(r.value) != 0:
				q &= Q(project_type__id=int(r.value))
			r= TryGetParam(request,'waitsubmit')
			if r:
				q&=Q(status=StatusApprove.WAIT_SUBMIT)
			else:
				q&=(~Q(status=StatusApprove.WAIT_SUBMIT))
			return q
		elif IsExpert(user):
			pes= ProjectApplyExpert.objects.filter(expert_id=user.pk).values('apply_id')
			idApplys=[int(p['apply_id']) for p in pes]
			q =  Q(id__in=idApplys)
			r= TryGetParam(request,'waitoption')
			if r:
				q&=Q(status=StatusApprove.WAIT_EXPERT)
			else:
				q&=~Q(status=StatusApprove.WAIT_EXPERT)
			return q
		raise Http404

	Auth(request)
	project_apply_list = ('pk', 'project_name',
	                      'project_type__name', 'project_no', 'applicant_time', 'status','study_type_name','project_comple_time')
	start, limit = StartLimit(request)

	user_filert = ProjectApplyList(request)
	items = ProjectApply.objects.filter(user_filert).values(*project_apply_list)[start:limit]
	total = ProjectApply.objects.filter(user_filert).count()
	return CurPage(total, items)


@Ajax
def project_type_details(request):
	Auth(request, Const.ADMIN)
	kv = GetParam(request, 'id')
	return ProjectType.objects.filter(pk=int(kv['id'])).values(
		'pk', 'name', 'waring_day','max_project_num','allow_apply')[0]


@Ajax
def project_type_update(request):
	project_type_update = ('pk', 'name', 'waring_day','max_project_num')
	kv = GetParam(request, *project_type_update)
	p = ProjectType.objects.get(pk=int(kv['pk']))
	p.name = kv['name']
	p.max_project_num=int(kv['max_project_num'])
	r=TryGetParam(request,'allow_apply')
	p.allow_apply=True if r else False

	p.save()
	return CallBack(Const.OK)


@Ajax
def project_apply_add(request):
	"""提交立项申请"""
	values = (
	'project_name',
	#'project_title_name',
	'project_area_name',
	'project_type_id',
	'study_type_name',
	'reserch_type_name',
	'teacher_name_ss',
	'teacher_name_bs',
	'teacher_unit',
	'teacher_phone',
	'teacher_remark',
	'g__actor__name',
	'g__actor__job_zw',
	'g__actor__job_zc',
	'g__actor__degree',
	'g__actor__desc',
	'comple_desc',
	'total_money',
	'comple_time',
	#	        'feasibility_desc' ,
	'marketing_desc',
	'g__levelachive__start_time',
	'g__levelachive__end_time',
	'g__levelachive__name',
	'g__levelachive__atype',
	'g__levelachive__apply_user',
	'g__finalachive__end_time',
	'g__finalachive__name',
	'g__finalachive__atype',
	'g__finalachive__font_num',
	'g__finalachive__actor',
	'book_money',
	'book_money_dec',
	'reserch_money',
	'reserch_money_dec',
	'meet_money',
	'meet_money_dec',
	'computer_money',
	'computer_money_dec',
	'print_money',
	'print_money_dec',
	'manage_money',
	'manage_money_dec',
	'other_money',
	'other_money_dec',
	'file_code')

	user = Auth(request, Const.APPLICANT)
	if not user: raise Http404
	kv, group_kv = GetArrayParams(request, *values)

	levelachives = group_kv['levelachive'].values()
	finalachives = group_kv['finalachive'].values()
	actors = group_kv['actor'].values()
	filecode = kv['file_code']

	@transaction.commit_on_success
	def runTran():
		d = Document()
		d.doc = RawDoc(filecode)
		assert d.doc
		if Const.DEBUG: print 'doc 路径为空值'
		d.pdf = Const.HERE + '/media/project/' + filecode + '.pdf'
		d.project_no = filecode
		d.save()

		pa = ProjectApply()
		FillModel(kv, pa)
		pa.applicant = user
		pa.unit_id = user.unit_id
		pa.status = StatusApprove.WAIT_SUBMIT
		pa.project_no = pa.RawRrojectApplyNO()
		pa.document = d
		pa.save()

		t = ConvertPDFTask()
		t.documentid = int(d.pk)
		t.save()



		#添加参与者
		for akv in actors:
			pa.actors.add(FillModel(akv, ProjectActor()))
		#最终成果
		for fkv in finalachives:
			pa.final_achives.add(FillModel(fkv, FinalAchievement()))
		#阶段性成果
		for lkv in levelachives:
			pa.level_achives.add(FillModel(lkv, LevelAchievement()))

		pa.save()

	runTran()
	return CallBack('立项申请已经保存，等待提交!')


@Ajax
def mesage_waitpublist(request):
	mesage_waitpublist_values = ('pk', 'title', 'abstract', 'sender_name', 'sender_real_name',
	                       'sender_unit__name', 'send_time','is_read','content')
	user = Auth(request)
	start, limit = StartLimit(request)
	conditon=[Q(receiver_unit_id=user.unit_id),Q(is_read=False)]
	items = Message.objects.filter(*conditon).values(*mesage_waitpublist_values)[start:limit]
	total = Message.objects.filter(*conditon).count()
	return CurPage(total, items)

@Ajax
def message_list(request):
	message_list_values = ('pk', 'title', 'abstract', 'sender_name', 'sender_real_name',
	                       'sender_unit__name', 'send_time','is_read','content')
	user = Auth(request)
	start, limit = StartLimit(request)
	conditon=[Q(receiver_unit_id=user.unit_id),Q(is_read=True)]
	items = Message.objects.filter(*conditon).values(*message_list_values)[start:limit]
	total = Message.objects.filter(*conditon).count()
	return CurPage(total, items)

@Ajax
def message_sended_list(request):
	user=Auth(request,Const.ADMIN)
	if not user:raise Http404
	start, limit = StartLimit(request)
	items = Message.objects.filter(sender_id=user.id).values(
		'pk', 'title', 'abstract', 'sender_name', 'sender_real_name',
		'sender_unit__name', 'send_time','is_read','content')[start:limit]
	total = Message.objects.filter(sender_id=user.id).count()
	return CurPage(total, items)

@Ajax
#消息发布
def message_pub(request):
	user=Auth(request, Const.ADMIN)
	kv=GetParam(request,'pk','recv')
	recv=int(kv['recv'])
	m=Message.objects.get(pk=int(kv['pk']))
	m_new=m.CopyMessage()
	m_new.sender_id=user.id
	if recv==-1:
		m_new.receiver_unit_id=user.unit_id
		m_new.is_read=True
	else:
		m_new.is_read=False
		m_new.receiver_unit_id=recv
	m_new.save()
	return OK

@Ajax
def message_add(request):
	user = Auth(request, Const.ADMIN)
	message_add_values = ('title', 'abstract', 'receiver_unit_id', 'content')
	kv = GetParam(request, *message_add_values)
	m = Message()
	FillModel(kv, m)
	if m.receiver_unit_id==-1:
		m.receiver_unit_id=user.unit_id
		m.is_read=True
	m.AttachSender(user)
	m.save()
	return CallBack('消息已发送！')

from datetime import timedelta

@Ajax
def message_recvier_combo(request):
	user = Auth(request)
	if IsAdmin(user):
		condition=[
			   Q(status=StatusUnit.NORMAL),
		           Q(level__gte=user.unit.level),
		           Q(parent_unit__id=user.unit_id)]
		unit_combo_values = ('pk', 'name')
		items = Unit.objects.filter(*condition).\
		order_by('level').values(*unit_combo_values)
		result=[{
			'pk':-1,
		        'name':'本单位所有人'
		}]
		for i in items:
			result.append({
				'pk':i['pk'],
			        'name':i['name']
			})
		return Items(result)
	else:
		raise Http404



def message_details(request):
	user=Auth(request)
	if not user:raise Http404
	kv=GetParam(request,'pk')
	m=Message.objects.get(pk=int(kv['pk']))
	return render_to_response('message_details.html',{'obj':m})


@Ajax
def message_notify(request):
	user = Auth(request)
	reslut={}
	if IsApplicant(user):
		#查询项目申请人的所有项目
		appleys = ProjectApply.objects.filter(
			applicant_id=user.id,
			status=StatusApprove.SUCCESS).values('project_type__waring_day', 'comple_time','pk')
		warings = [a for a in appleys
		           if a['comple_time'] < datetime.now() + timedelta(days=a['project_type__waring_day'])]
		count = len(warings)
		if count: reslut['msg']='系统提示:<br/><br/>您当前已经有' + str(count) + '个项目处于预警状态!<br/><br/>请查看项目预警列表'
		ws=[]
		for w in warings:
			ws.append(str(w['pk']))
		reslut['warings']=','.join(ws)

	user.last_activity_date=datetime.now()
	user.last_activity_ip=user.get_client_ip(request)
	user.save()


	minTime=datetime.now()-timedelta(seconds=60)
	onlinecount=User.objects.filter(last_activity_date__gt=minTime).count()
	reslut['onlinecount']=onlinecount
	reslut['logincount']=user.login_count
	reslut['lastip']=user.last_activity_ip

	return reslut


@Ajax
def project_apply_submit(request):
	kv = GetParam(request, 'ids')
	if Auth(request, Const.APPLICANT):
		ProjectApply.objects.filter(id__in=IdArray(kv['ids'])).\
		update(status=StatusApprove.WAIT_ADMIN_2)
		return CallBack(Const.OK)
@Ajax
def project_apply_all_approves(request):
	if not Auth(request):return
	kv=GetParam(request,'pk')
	start, limit = StartLimit(request)
	items=ProjectApplyApprove.objects.filter(details_id=int(kv['pk'])).\
	values('approve__name',
		'approve__role__name',
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'approve_opinion','success')[start:limit]
	count=ProjectApplyApprove.objects.filter(details_id=int(kv['pk'])).count()
	return CurPage(count,items)

@Ajax
def project_end_all_approves(request):
	if not Auth(request):return
	kv=GetParam(request,'pk')
	start, limit = StartLimit(request)
	items=ProjectEndApplyApprove.objects.filter(details_id=int(kv['pk'])).\
	      values('approve__name',
		'approve__role__name',
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'approve_opinion','success')[start:limit]
	count=ProjectEndApplyApprove.objects.filter(details_id=int(kv['pk'])).count()
	return CurPage(count,items)

@Ajax
def project_exchange_all_approves(request):
	if not Auth(request):return
	kv=GetParam(request,'pk')
	start, limit = StartLimit(request)
	items=ProjectExChangeApprove.objects.filter(details_id=int(kv['pk'])).\
	      values('approve__name',
		'approve__role__name',
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'approve_opinion','success')[start:limit]
	count=ProjectExChangeApprove.objects.filter(details_id=int(kv['pk'])).count()
	return CurPage(count,items)

@Ajax
def project_back_all_approves(request):
	if not Auth(request):return
	kv=GetParam(request,'pk')
	start, limit = StartLimit(request)
	items=ProjectRollbackApplyApprove.objects.filter(details_id=int(kv['pk'])).\
	      values('approve__name',
		'approve__role__name',
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'approve_opinion','success')[start:limit]
	count=ProjectRollbackApplyApprove.objects.filter(details_id=int(kv['pk'])).count()
	return CurPage(count,items)

#show admin those
@Ajax
def project_admin_apply_all_approves(request):
	user= Auth(request,Const.ADMIN)
	start, limit = StartLimit(request)
	kv=GetParam(request,'pass','build')
	condition=Q(approve_id=user.id)
	success=int(kv['pass'])
	if success==1:
		condition&=Q(success=True)
	elif success==0:
		condition&=Q(success=False)

	build=int(kv['build'])
	if build==1:
		condition&=~Q(details__project_id=0)
	elif build==0:
		condition&=Q(details__project_id=0)

	items=ProjectApplyApprove.objects.filter(condition).\
	      values(

		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'details__project_name',
		'details__project_no',
		'approve_opinion','success')[start:limit]
	count=ProjectApplyApprove.objects.filter(condition).count()
	return CurPage(count,items)


def download_project_admin_apply_all_approves_excel(request):
	user= Auth(request,Const.ADMIN)
	condition=Q(approve_id=user.id)
	condition&=~Q(details__project_id=0)
	renders=[
		ExcelRender('项目编号','details__project_no'),
		ExcelRender('审核单位','approve__unit__name'),
	        ExcelRender('单位级别', 'approve__unit__level',lambda x:UnitLevel.get(x,'未知级别')),
	        ExcelRender('审核时间', 'approvetime',lambda x:x.strftime('%Y年%m月%d日')),
		ExcelRender('项目名称','details__project_name'),
		ExcelRender('审核意见','approve_opinion'),
		ExcelRender('审核结果','success',lambda x:'通过' if x else '不通过')
	]

	items=ProjectApplyApprove.objects.filter(condition).\
	      values(
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'details__project_name',
		'details__project_no',
		'approve_opinion','success')
	return  WriteDictToExcel(items,renders)

@Ajax
def project_admin_end_all_approves(request):
	user= Auth(request,Const.ADMIN)
	start, limit = StartLimit(request)
	condition=Q(approve_id=user.id)
	kv=GetParam(request,'pass')
	success=int(kv['pass'])
	if success==1:
		condition&=Q(success=True)
	elif success==0:
		condition&=Q(success=False)

	items=ProjectEndApplyApprove.objects.filter(condition).\
	      values(
		'details__project__name',
		'details__project__no',
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'approve_opinion',
		'success')[start:limit]

	count=ProjectEndApplyApprove.objects.filter(condition).count()
	return CurPage(count,items)

@Ajax
def project_admin_exchange_all_approves(request):
	user= Auth(request,Const.ADMIN)
	start, limit = StartLimit(request)
	kv=GetParam(request,'pass')
	condition=Q(approve_id=user.id)
	success=int(kv['pass'])
	if success==1:
		condition&=Q(success=True)
	elif success==0:
		condition&=Q(success=False)

	items=ProjectExChangeApprove.objects.filter(condition).\
	      values(
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'details__project__name',
		'details__project__no',
		'approve_opinion','success')[start:limit]
	count=ProjectExChangeApprove.objects.filter(condition).count()
	return CurPage(count,items)

@Ajax
def project_admin_back_all_approves(request):
	user= Auth(request,Const.ADMIN)
	start, limit = StartLimit(request)
	items=ProjectRollbackApplyApprove.objects.filter(approve_id=user.id).\
	      values(
		'approve__unit__name',
		'approve__unit__level',
		'approvetime',
		'details__project__name',
		'details__project__no',
		'approve_opinion','success')[start:limit]
	count=ProjectRollbackApplyApprove.objects.filter(approve_id=user.id).count()
	return CurPage(count,items)


@Ajax
def project_apply_details(request):
	kv=GetParam(request,'pk')
	pk=int(kv['pk'])
	return {
		'levelachives':LevelAchievement.objects.filter(apply_id=pk).values(
			'start_time',
			'end_time',
			'name',
			'atype',
			'apply_user'),
	        'finalachives':FinalAchievement.objects.filter(apply_id=pk).values(
		        'end_time',
		        'name',
		        'atype',
		        'font_num',
		        'actor',
	        ),
		'actors':ProjectActor.objects.filter(apply_id=pk).values(
			'name',
			'job',
			'degree',
			'desc',
		),
		'apply':ProjectApply.objects.filter(id=pk).values('project_name',
			#'project_title_name',
			'project_type_id',
			'project_area_name',
			'study_type_name',
			'reserch_type_name',
			'teacher_name_ss',
			'teacher_name_bs',
			'teacher_unit',
			'teacher_phone',
			'teacher_remark',
			'comple_desc',
			'total_money',
			'comple_time',
			'marketing_desc',
			'book_money',
			'book_money_dec',
			'reserch_money',
			'reserch_money_dec',
			'meet_money',
			'meet_money_dec',
			'computer_money',
			'computer_money_dec',
			'print_money',
			'print_money_dec',
			'manage_money',
			'manage_money_dec',
			'other_money',
			'other_money_dec',
			'file_code')[0]
	}



@Ajax
def project_apply_approve(request):
	def ProceedApprove(user, success):
		if IsAdmin(user):
			if user.unit.level == 0:
				#科技局查看 项目审查
				kv=GetParam(request,'wait_admin_look')
				if int(kv['wait_admin_look'])==1:
					return StatusApprove.WAIT_SET_EXPERT if success else StatusApprove.WAIT_SUBMIT
				else:
					#审核
					return StatusApprove.SUCCESS if success else StatusApprove.WAIT_SUBMIT

			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				#return StatusApprove.WAIT_SET_EXPERT if success else StatusApprove.FAILED_ADMIN_1
				return StatusApprove.WAIT_AMIDN_0_LOOK if success else StatusApprove.WAIT_SUBMIT
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				#return StatusApprove.WAIT_ADMIN_1 if success else StatusApprove.FAILED_ADMIN_2
				return StatusApprove.WAIT_ADMIN_1 if success else StatusApprove.WAIT_SUBMIT

		elif IsExpert(user):
			#专家转管理员审核
			return StatusApprove.WAIT_ADMIN_0

		raise Http404

	#项目申请审核
	user = Auth(request)
	kv = GetParam(request, 'ids', 'pass', 'option')
	success = bool(kv['pass'] == 'true')
	option = kv['option']
	approve_status = ProceedApprove(user, success)
	now, idArr = datetime.now(), IdArray(kv['ids'])
	if IsAdmin(user) or IsExpert(user):
		ProjectApply.objects.filter(id__in=idArr).update(status=approve_status)
		applys = ProjectApply.objects.filter(id__in=idArr)
		bulk = [ProjectApplyApprove(
			approve=user,
			approvetime=now,
			approve_opinion=kv['option'],
			success=success,
			details=p) for p in applys]
		ProjectApplyApprove.objects.bulk_create(bulk)
		#项目立项申请通过
		if approve_status == StatusApprove.SUCCESS:
			for p in applys: p.CreateProject()

	if IsExpert(user):
		expert_percent=TryGetParam(request,'expert_percent')
		ProjectApply.objects.filter(id__in=idArr).update(
			status=approve_status,
			expert_success=success,
			expert_percent=expert_percent.value,
			expert_approve_time=now,
			expert_opinion=option)

	return CallBack('审核成功！' + ApproveStatus.get(approve_status))



@Ajax
def project_exchange_approve(request):
	def ProceedApprove(user, success):
		if IsAdmin(user):
			if user.unit.level == 0:
				#科技局查看 待审核
				return StatusApprove.SUCCESS if success else StatusApprove.FAILED_ADMIN_0
			elif user.unit.level == 1:
				#一级单位查看 子部门 待审核
				return StatusApprove.WAIT_ADMIN_0 if success else StatusApprove.FAILED_ADMIN_1
			elif user.unit.level == 2:
				#二级单位管理员 待审核
				return StatusApprove.WAIT_ADMIN_1 if success else StatusApprove.FAILED_ADMIN_2
		raise Http404

	#项目变更审核
	user = Auth(request, Const.ADMIN)
	if user:
		kv = GetParam(request, 'ids', 'pass', 'option')
		success = bool(kv['pass'] == 'true')
		approve_status = ProceedApprove(user, success)
		bulk, now, idArr = [], datetime.now(), IdArray(kv['ids'])
		ProjectExChange.objects.filter(id__in=idArr).update(status=approve_status)
		exchanges = ProjectExChange.objects.filter(id__in=idArr)

		bulk = [ProjectExChangeApprove(
			approve=user,
			approvetime=now,
			details=p,
			approve_opinion=kv['option'],
			success=success) for p in exchanges]
		ProjectExChangeApprove.objects.bulk_create(bulk)

		#项目变更申请通过
		if approve_status == StatusApprove.SUCCESS:
			for p in exchanges:
				p.project.status = p.forward_status
				if p.forward_status==StatusProject.LAZY:
					p.project.comple_time=p.new_project_end_date

				p.project.save()
		return CallBack('审核成功！' + ApproveStatus.get(approve_status))
	else:
		raise Http404


#
#def raw_project_apply_doc(request,pk):
#
#	Auth(request)
#	p=ProjectApply.objects.get(id=int(pk))
#	return p.WORD()
#
#def raw_project_apply_pdf(request,pk):
#
#	Auth(request)
#	p=ProjectApply.objects.get(id=int(pk))
#	return p.WORD()
#
#
#def raw_doc(request,url):
#	Auth(request)
#	return render_to_response('word.html',{'url': 'http://'+request.get_host()+'/'+url})
#
#def raw_pdf(request,url):
#	Auth(request)
#	return render_to_response('pdf.html',{'url': 'http://'+request.get_host()+'/'+url})

def download_document(request,pk):
	Auth(request)
	try:
		p = Document.objects.get(pk=pk)
	except:
		raise Http404
	if not os.path.exists(p.pdf): raise Http404
	def Writer():
		with open(p.pdf, 'rb') as f:
			while 1:
				buf = f.read(65536)
				if not buf: break
				yield buf

	response = HttpResponse(Writer(), content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=document.pdf'
	return response

def download_project_apply_pdf(request, pk):
	Auth(request)
	try:
		p = ProjectApply.objects.get(pk=pk)
		pdf = p.document.pdf
	except:
		raise Http404
	if not os.path.exists(pdf): raise Http404

	def Writer():
		with open(pdf, 'rb') as f:
			while 1:
				buf = f.read(65536)
				if not buf: break
				yield buf

	response = HttpResponse(Writer(), content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=document.pdf'
	return response


def upload_project_apply_doc(request):
	user=Auth(request)
	filecode=ProjectApply.RawUploadRrojectApplyNO(user.unit)
	ext = request.POST.get('ext')
	doc = Const.HERE + '/media/project/' + filecode + ext
	def handle_uploaded_file(f):
		with open(doc, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
	handle_uploaded_file(request.FILES['file'])
	ret_json = {'success': True, 'code': filecode}
	return HttpResponse(dumps(ret_json))


def download_project_apply_doc_temp(request):
	Auth(request)

	def Writer():
		with open(Const.HERE + '/static/word/项目申请书.doc', 'rb') as f:
			while 1:
				buf = f.read(65536)
				if not buf: break
				yield buf

	response = HttpResponse(Writer(), content_type='application/vnd.ms-word')
	response['Content-Disposition'] = 'attachment; filename=document.doc'
	return response


def raw_code(request):
	import ImageFont, Image, ImageDraw, random
	from cStringIO import StringIO

	string = {'number': '12345679',
	          'litter': 'ACEFGHKMNPRTUVWXY'}
	background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
	line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
	img_width = 58
	img_height = 30
	font_color = ['black', 'darkblue', 'darkred']
#	font_size = 14
	font =Const.CodeFont()
	request.session['verify'] = ''
	#新建画布
	im = Image.new('RGB', (img_width, img_height), background)
	code = random.sample(string['litter'], 4)
	#新建画笔
	draw = ImageDraw.Draw(im)
	#画干扰线
	for i in range(random.randrange(3, 5)):
		xy = (random.randrange(0, img_width), random.randrange(0, img_height),
		      random.randrange(0, img_width), random.randrange(0, img_height))
		draw.line(xy, fill=line_color, width=1)
	#写入验证码文字
	x = 2
	for i in code:
		y = random.randrange(0, 10)
		draw.text((x, y), i, font=font, fill=random.choice(font_color))
		x += 14
		request.session['verify'] += i
	del draw
	buf = StringIO()
	im.save(buf, 'gif')
	buf.seek(0)
	return HttpResponse(buf.getvalue(), 'image/gif')




