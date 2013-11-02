#coding=utf-8
from datetime import datetime
import os
import traceback
from django.db import models, transaction
from django.http import HttpResponse
from science import settings
from science.settings import MEDIA_ROOT
from tools.const import UnitLevel, Const, StatusProject, ConvertStatus, StatusConvert, UnitNo, ProjectArea, StatusApprove
from tools.helper import  Guid, TimeNow, YMD
from core.word_templates import WordTemplates


class Role(models.Model):
	#相当于varchar字符类型
	name = models.CharField(verbose_name='角色名', max_length=25)
	code= models.CharField(verbose_name='编码', max_length=25)
	level = models.IntegerField(verbose_name='权限等级',default=0)
	#重载meta模块,修改Admin后台中显示的名称
	class Meta:
		verbose_name = '角色'
		verbose_name_plural = '角色列表'

	def __unicode__(self):
		return self.name

class ProjectType(models.Model):
	name = models.CharField(verbose_name='项目类型', max_length=25)
	waring_day=models.IntegerField(verbose_name='预警项目',default=20)
	allow_apply= models.BooleanField(
		verbose_name='是否允许申报',
		choices=((True, '允许'), (False, '不允许')), default=1)
	max_project_num=models.IntegerField(verbose_name='最大项目数量',default=0)
	#重载meta模块,修改Admin后台中显示的名称
	class Meta:
		verbose_name = '项目类型'
		verbose_name_plural = '项目类型列表'


	def __unicode__(self):
		return self.name


class Unit(models.Model):
	name = models.CharField(verbose_name='单位名', max_length=25)
	parent_unit = models.ForeignKey('self', blank=True,null=True, verbose_name='所属单位',default=0)
	address = models.CharField(verbose_name='单位地址', max_length=25)
	phone = models.CharField(verbose_name='单位电话', max_length=25,default='')

	status = models.IntegerField(verbose_name='单位状态Code',default=0)
	level=models.IntegerField(verbose_name='单位级别',default=0)
	regtime=models.DateTimeField(verbose_name='注册时间',default=datetime.now, blank=True)

#	project_type = models.ForeignKey(ProjectType, verbose_name='申请项目类型',
#		related_name='+',default=0, blank=True,null=True,)

	max_project = models.IntegerField(verbose_name='申请项目最大数量',default=0)
	apply_starttime=models.DateTimeField(verbose_name='申报开始时间',default=datetime.now, blank=True)
	apply_endtime=models.DateTimeField(verbose_name='申报结束时间',default=datetime.now, blank=True)
	no= models.CharField(verbose_name='单位编号', max_length=25,default='')

	faren= models.CharField(verbose_name='法人', max_length=50,default='')
	zipcode= models.CharField(verbose_name='邮政编码', max_length=50,default='')

	class Meta:
		verbose_name = '单位'
		verbose_name_plural = '单位列表'

	def save(self, force_insert=False, force_update=False, using=None):

		if self.parent_unit is None:
			self.level=0
		else:
			self.level=0
			parent=self.parent_unit
			while parent:
				self.level+=1
				parent=parent.parent_unit
				if not parent:break
				if parent.id==self.id:break

		models.Model.save(self, force_insert, force_update, using)



	def __unicode__(self):
		return self.name

	def __get_level_name(self):
		return UnitLevel.get(self.level,'超出单位级别')

	level_name=property(__get_level_name)


class UnitLimitProjectType(models.Model):
	unit = models.ForeignKey(Unit, verbose_name='所属单位', related_name='+',default=0)
	project_type=models.ForeignKey(ProjectType, verbose_name='项目类型', related_name='+',default=0)
	max_project_num=models.IntegerField(verbose_name='最大申请数目',default=0)

class User(models.Model):
	name = models.CharField(verbose_name='用户名', max_length=25)
	real_name = models.CharField(verbose_name='真实姓名', max_length=25)
	password = models.CharField(verbose_name='密码', max_length=50)

	email=models.CharField(verbose_name='邮件', max_length=50,default='')
	identitycard=models.CharField(verbose_name='身份证', max_length=50,default='')

	job_admin_name= models.CharField(verbose_name='行政职务', max_length=25,default='')
	job_name= models.CharField(verbose_name='专业职务', max_length=25,default='')
	last_degree=models.CharField(verbose_name='最后学位', max_length=25,default='')

	nation_name= models.CharField(verbose_name='民族', max_length=25,default='')
	research_speciality= models.CharField(verbose_name='研究专长', max_length=25,default='')
	study_type_name = models.CharField(verbose_name='学科分类', max_length=25,default='')

	#相当于varchar字符类型
	sex = models.BooleanField(verbose_name='性别',
		choices=((False, "女"), (True, "男")), default=1)
	phone = models.CharField(max_length=25, verbose_name='电话')
	mobile = models.CharField(max_length=25, verbose_name='手机')
	unit = models.ForeignKey(Unit, verbose_name='所属单位', related_name='+',default=0)
	role = models.ForeignKey(Role, verbose_name='角色', related_name='+',default=0)
	remark = models.TextField(max_length=200, verbose_name='备注信息')
	status = models.IntegerField(verbose_name='用户状态Code',default=0)
	regtime=models.DateTimeField(verbose_name='注册时间',default=datetime.now, blank=True)

	approve_time=models.DateTimeField(verbose_name='审核时间',default=datetime.now, blank=True)
	approve_opinion=models.DateTimeField(verbose_name='审核意见',default=datetime.now, blank=True)

	login_count = models.IntegerField(verbose_name='登录次数',default=0)

	last_activity_ip = models.CharField(max_length=25, verbose_name='登录ip地址',default='')
	last_activity_date = models.DateTimeField(default = datetime(1950, 1, 1))

	orgcode = models.CharField(max_length=50, verbose_name='组织机构代码',default='')
	jobunit = models.CharField(max_length=50, verbose_name='业务部门',default='')

	def get_client_ip(self,request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip

	#重载meta模块,修改Admin后台中显示的名称
	class Meta:
		verbose_name = '用户'
		verbose_name_plural = '用户列表'

	def __unicode__(self):
		return self.name

	def _get_role_name(self):
		if self.role.code==Const.ADMIN and self.unit.level==0:
			return '国家民委管理员'
		elif self.role.code==Const.ADMIN and self.unit.level==1:
			return '一级单位管理员'
		elif self.role.code==Const.ADMIN and self.unit.level==2:
			return '二级单位管理员'
		else:
			return self.role.name

	def _get_detail_name(self):
		return self.name+'<'+self.real_name+'>'

	def _get_sex_name(self):
		return '男' if self.sex else '女'

	role_name=property(_get_role_name)
	detail_name=property(_get_detail_name)
	sex_name=property(_get_sex_name)






class Message(models.Model):
	title = models.CharField(verbose_name='单位名', max_length=25,default='')
	content = models.TextField(max_length=200, verbose_name='消息内容',default='')
	abstract= models.CharField(verbose_name='消息摘要', max_length=25,default='')

	sender_unit = models.ForeignKey(Unit, verbose_name='发送单位', related_name='+',default=0)
	receiver_unit = models.ForeignKey(Unit, verbose_name='接受单位', related_name='+',default=0)
	sender_id=models.IntegerField(verbose_name='发送人ID',default=0)
	sender_name=models.CharField(verbose_name='发送人', max_length=50,default='')
	sender_real_name=models.CharField(verbose_name='发送人姓名', max_length=50,default='')

	send_time=models.DateTimeField(verbose_name='发送时间',default=datetime.now, blank=True)
	is_read= models.BooleanField(choices=((True, '已读'), (False, '未读')), default=0)


	def CopyMessage(self):
		m=Message()
		m.title=self.title
		m.content=self.content
		m.abstract=self.abstract
		m.sender_unit=self.sender_unit
		m.receiver_unit=self.receiver_unit
		m.sender_name=self.sender_name
		m.sender_real_name=self.sender_real_name
		m.send_time=self.send_time
		m.is_read=self.is_read
		return m

	def AttachSender(self,user):
		self.sender_name=user.name
		self.sender_real_name=user.real_name
		self.sender_unit_id=user.unit_id
		self.sender_id=user.pk

	#重载meta模块,修改Admin后台中显示的名称
	class Meta:
		verbose_name = '消息'
		verbose_name_plural = '消息列表'

	def __unicode__(self):
		return self.abstract

	def save(self, force_insert=False, force_update=False, using=None):
		#todo send email


		models.Model.save(self, force_insert, force_update, using)

class Document(models.Model):

	project_no=models.CharField(verbose_name='文档版本', max_length=25,default='')

	create_time=models.DateTimeField(verbose_name='文档创建时间',default=datetime.now, blank=True)

	pdf=models.CharField(verbose_name='pdf', max_length=25,default='')
	doc=models.CharField(verbose_name='doc', max_length=25,default='')

	converted=models.IntegerField(verbose_name='文档转换状态',default=0)
	converted_err=models.TextField(verbose_name='转换错误信息',default='')

	def _get_convert_status(self):
		return ConvertStatus.get(self.converted,'转换失败')

	def _set_convert_status(self,value):
		self.converted=value

	convert_status=property(_get_convert_status,_set_convert_status)

	class Meta:
		verbose_name = '文档'
		verbose_name_plural = '文档列表'

	def __unicode__(self):
		return u'文档'


class Project(models.Model):
	name = models.CharField(verbose_name='项目名称', max_length=25)
	ptype = models.ForeignKey(ProjectType, verbose_name='项目类型', related_name='+',default=0)
	no = models.CharField(verbose_name='项目代号', max_length=25)

	applicant = models.ForeignKey(User, verbose_name='申请人', related_name='+',default=0)
	applicant_time=models.DateTimeField(verbose_name='申报时间',default=datetime.now, blank=True)
	applicant_opinion= models.TextField(max_length=200, verbose_name='申请原因',default='')
	unit=models.ForeignKey(Unit, verbose_name='所属单位', related_name='+',default=0)
	status = models.IntegerField( verbose_name='项目状态')
	project_area_name= models.CharField(verbose_name='项目领域', max_length=25,default='')

	project_title_name = models.CharField(verbose_name='课题名称', max_length=25,default='')
	study_type_name = models.CharField(verbose_name='学科分类', max_length=25,default='')
	reserch_type_name= models.CharField(verbose_name='研究类型', max_length=25,default='')


	teacher_name_ss= models.CharField(verbose_name='硕士生导师', max_length=25,default='')
	teacher_name_bs= models.CharField(verbose_name='博士生导师', max_length=25,default='')

	teacher_unit= models.CharField(verbose_name='担任导师单位', max_length=25,default='')
	teacher_phone=models.CharField(verbose_name='担任导师电话', max_length=25,default='')
	teacher_remark=models.TextField(max_length=200, verbose_name='导师研究成果',default='')


	expert=models.ForeignKey(User, verbose_name='专家评审', related_name='+',default=0)
	expert_success = models.BooleanField(choices=((True, '同意'), (False, '不同意')), default=0)
	expert_approve_time=models.DateTimeField(verbose_name='专家评审时间',default=datetime.now, blank=True)
	expert_opinion= models.TextField(max_length=200, verbose_name='专家意见',default='')



	total_money=models.IntegerField( verbose_name='经费(万元)',default=0)
	book_money=models.IntegerField( verbose_name='资料费',default=0)
	book_money_dec= models.TextField(max_length=200, verbose_name='资料费描述',default='')

	reserch_money=models.IntegerField( verbose_name='国内调研差旅费',default=0)
	reserch_money_dec= models.TextField(max_length=200, verbose_name='国内调研差旅费描述',default='')

	meet_money=models.IntegerField( verbose_name='小型会议费',default=0)
	meet_money_dec= models.TextField(max_length=200, verbose_name='小型会议费描述',default='')

	computer_money=models.IntegerField( verbose_name='计算机使用费',default=0)
	computer_money_dec= models.TextField(max_length=200, verbose_name='计算机使用费描述',default='')

	print_money=models.IntegerField( verbose_name='印刷补助费',default=0)
	print_money_dec= models.TextField(max_length=200, verbose_name='印刷补助费描述',default='')

	manage_money=models.IntegerField( verbose_name='管理费',default=0)
	manage_money_dec= models.TextField(max_length=200, verbose_name='管理费描述',default='')

	other_money=models.IntegerField( verbose_name='其他经费',default=0)
	other_money_dec= models.TextField(max_length=200, verbose_name='其他描述',default='')

	comple_time=models.DateTimeField(verbose_name='预期完成时间',default=datetime.now, blank=True)
	comple_desc=models.TextField(max_length=500, verbose_name='预期成果描述',default='')

	feasibility_desc=models.TextField(max_length=500, verbose_name='可行性论证',default='')
	marketing_desc=models.TextField(max_length=500, verbose_name='应用推广或市场分析',default='')

	document=models.ForeignKey(Document, verbose_name='相关材料', related_name='+',default=0)

	class Meta:
		verbose_name = '项目'
		verbose_name_plural = '项目列表'

	def __unicode__(self):
		return self.name




class ProjectApply(models.Model):
	applicant=models.ForeignKey(User,verbose_name='审核人',related_name='+',default=0)
	applicant_opinion= models.TextField(max_length=200, verbose_name='申请原因',default='')
	applicant_time=models.DateTimeField(verbose_name='申请时间',default=datetime.now, blank=True)

	forward_status=models.IntegerField(verbose_name='审核通过状态',default=0)
	backward_status=models.IntegerField(verbose_name='项目当前状态',default=0)

	project_name = models.CharField(verbose_name='项目名称', max_length=25,default='')
	project_area_name= models.CharField(verbose_name='项目领域', max_length=25,default='')

	project_title_name = models.CharField(verbose_name='课题名称', max_length=25,default='')
	study_type_name = models.CharField(verbose_name='学科分类', max_length=25,default='')
	reserch_type_name= models.CharField(verbose_name='研究类型', max_length=25,default='')

	teacher_name_ss= models.CharField(verbose_name='硕士生导师', max_length=25,default='')
	teacher_name_bs= models.CharField(verbose_name='博士生导师', max_length=25,default='')

	teacher_unit= models.CharField(verbose_name='担任导师单位', max_length=25,default='')
	teacher_phone=models.CharField(verbose_name='担任导师电话', max_length=25,default='')
	teacher_remark=models.TextField(max_length=200, verbose_name='导师研究成果',default='')

	project_type = models.ForeignKey(ProjectType, verbose_name='项目类型', related_name='+',default=0)
	project_no = models.CharField(verbose_name='项目代号', max_length=25,default=Guid)
	status = models.IntegerField( verbose_name='申请状态',default=0)
	unit=models.ForeignKey(Unit, verbose_name='所属单位', related_name='+',default=0)

	#expert=models.ForeignKey(User, verbose_name='专家评审', related_name='+',default=0)


	total_money=models.IntegerField( verbose_name='经费(万元)',default=0)
	book_money=models.IntegerField( verbose_name='资料费',default=0)
	book_money_dec= models.TextField(max_length=200, verbose_name='资料费描述',default='')

	reserch_money=models.IntegerField( verbose_name='国内调研差旅费',default=0)
	reserch_money_dec= models.TextField(max_length=200, verbose_name='国内调研差旅费描述',default='')

	meet_money=models.IntegerField( verbose_name='小型会议费',default=0)
	meet_money_dec= models.TextField(max_length=200, verbose_name='小型会议费描述',default='')

	computer_money=models.IntegerField( verbose_name='计算机使用费',default=0)
	computer_money_dec= models.TextField(max_length=200, verbose_name='计算机使用费描述',default='')

	print_money=models.IntegerField( verbose_name='印刷补助费',default=0)
	print_money_dec= models.TextField(max_length=200, verbose_name='印刷补助费描述',default='')

	manage_money=models.IntegerField( verbose_name='管理费',default=0)
	manage_money_dec= models.TextField(max_length=200, verbose_name='管理费描述',default='')

	other_money=models.IntegerField( verbose_name='其他经费',default=0)
	other_money_dec= models.TextField(max_length=200, verbose_name='其他描述',default='')

	comple_time=models.DateTimeField(verbose_name='预期完成时间',default=datetime.now, blank=True)
	comple_desc=models.TextField(max_length=500, verbose_name='预期成果描述',default='')

	feasibility_desc=models.TextField(max_length=500, verbose_name='可行性论证',default='')
	marketing_desc=models.TextField(max_length=500, verbose_name='应用推广或市场分析',default='')

	document=models.ForeignKey(Document, verbose_name='相关材料', related_name='+',default=0)
	file_code=models.CharField(verbose_name='文件编号', max_length=25,default='')
	project_id=models.IntegerField( verbose_name='项目ID',default=0)
	project_comple_time=models.DateTimeField(verbose_name='项目完成时间', default=datetime.now, blank=True)

	expert_percent=models.CharField(verbose_name='专家平均分',default='0',max_length=25)
	expert_names=models.CharField(verbose_name='送审专家', max_length=500,default='')


	expert_post_num=models.IntegerField(verbose_name='送审',default=0)
	expert_recv_num=models.IntegerField(verbose_name='接收',default=0)

	expert_success = models.BooleanField(choices=((True, '同意'), (False, '不同意')), default=0)
	expert_approve_time=models.DateTimeField(verbose_name='专家评审时间',default=datetime.now, blank=True)
	expert_opinion= models.TextField(max_length=200, verbose_name='专家意见',default='')
	admin_support_result=models.CharField(verbose_name='资助选项', max_length=50,default='')

	def RePercent(self,expert_percent):
		new_percetn=(float(self.expert_percent)*self.expert_post_num
		                     +float(expert_percent))/(self.expert_post_num+1)
		new_percetn=round(new_percetn,3)
		self.expert_percent="%.3f" % new_percetn
		self.expert_post_num+=1
		if self.expert_post_num>=self.expert_recv_num:
			self.status=StatusApprove.WAIT_ADMIN_0
		self.save()

	class Meta:
		verbose_name = '项目申请'
		verbose_name_plural = '项目申请列表'



	def RawProjectNO(self):
		@transaction.commit_on_success
		def tran():
			year=datetime.now().year
			unit=self.applicant.unit
			count=Project.objects.filter(applicant_time__year=year).count()
			area=ProjectArea.get(self.project_area_name,'')
			#部门编号大写
			uno= ''.join([i for i in unit.no if i.isupper()])
			new_no='MW'+ area +'%s%s%03d' % (str(year)[2:], uno,count+1)
			return new_no
		return tran()

	@staticmethod
	def RawUploadRrojectApplyNO(unit):
		@transaction.commit_on_success
		def tran():
			year=datetime.now().year
			count=ProjectApply.objects.filter(applicant_time__year=year).count()
			#部门编号大写
			uno= ''.join([i for i in unit.no if i.isupper()])
			new_no='AMW' +'%s%s%03d' % (str(year)[2:],uno,count+1)
			return new_no
		return tran()

	def RawRrojectApplyNO(self):
		@transaction.commit_on_success
		def tran():
			year=datetime.now().year
			unit=self.applicant.unit
			count=ProjectApply.objects.filter(applicant_time__year=year).count()
			area=ProjectArea.get(self.project_area_name,'')
			#部门编号大写
			uno= ''.join([i for i in unit.no if i.isupper()])
			new_no='AMW' +area+'%s%s%03d' % (str(year)[2:],uno,count+1)
			return new_no
		return tran()

	def GetProject(self):
		return None if self.project_id==0 else Project.objects.get(pk=self.project_id)

	def CreateProject(self):
		p=Project()
		p.name=self.project_name
		p.ptype=self.project_type
		p.applicant=self.applicant
		p.no =self.RawProjectNO()
		p.unit_id=self.applicant.unit_id
		p.status=StatusProject.NORMAL
		p.project_area_name=self.project_area_name
		p.applicant_time=self.applicant_time
		p.applicant_opinion= self.applicant_opinion

		p.project_title_name = self.project_title_name
		p.study_type_name =self. study_type_name
		p.reserch_type_name=self.reserch_type_name

		p.teacher_name_ss= self.teacher_name_ss
		p.teacher_name_bs= self.teacher_name_bs

		p.teacher_unit=self.teacher_unit
		p.teacher_phone=self.teacher_phone
		p.teacher_remark=self.teacher_remark

		#p.expert=self.expert
		p.expert_success = self.expert_success
		p.expert_approve_time=self.expert_approve_time
		p.expert_opinion= self.expert_opinion

		p.total_money=self.total_money
		p.book_money=self.book_money
		p.book_money_dec=self. book_money_dec

		p.reserch_money=self.reserch_money
		p.reserch_money_dec= self.reserch_money_dec

		p.meet_money=self.meet_money
		p.meet_money_dec= self.meet_money_dec

		p.computer_money=self.computer_money
		p.computer_money_dec= self.computer_money_dec

		p.print_money=self.print_money
		p.print_money_dec=self.print_money_dec

		p.manage_money=self.manage_money
		p.manage_money_dec=self.manage_money_dec

		p.other_money=self.other_money
		p.other_money_dec= self.other_money_dec

		p.comple_time=self.comple_time
		p.comple_desc=self.comple_desc

		p.feasibility_desc=self.feasibility_desc
		p.marketing_desc=self.marketing_desc
		p.document=self.document
		p.save()
		self.project_comple_time=self.comple_time
		self.project_id=p.id
		self.save()

	def __unicode__(self):
		return self.project_name


class ProjectExChange(models.Model):
	applicant=models.ForeignKey(User,verbose_name='审核人',related_name='+',default=0)
	applicant_opinion= models.TextField(max_length=200, verbose_name='申请原因',default='')
	applicant_time=models.DateTimeField(verbose_name='申请时间',default=datetime.now, blank=True)

	forward_status=models.IntegerField(verbose_name='审核通过状态',default=0)
	backward_status=models.IntegerField(verbose_name='项目当前状态',default=0)

	project=models.ForeignKey(Project, verbose_name='项目详情', related_name='+',default=0)
	project_name = models.CharField(verbose_name='项目名称', max_length=25,default='')
	project_type = models.ForeignKey(ProjectType, verbose_name='项目类型', related_name='+',default=0)
	project_no = models.CharField(verbose_name='项目代号', max_length=25,default='')
	project_status=models.IntegerField( verbose_name='项目状态',default=0)

	new_project_end_date=models.DateTimeField(verbose_name='延期时间',default=datetime.now, blank=True)

	status = models.IntegerField( verbose_name='申请状态',default=0)
	unit=models.ForeignKey(Unit, verbose_name='所属单位', related_name='+',default=0)

	def save(self, force_insert=False, force_update=False, using=None):
		self.project_name = self.project.name
		self.project_type = self.project.ptype
		self.project_no = self.project.no
		self.project_status=self.project.status
		models.Model.save(self, force_insert, force_update, using)

	class Meta:
		verbose_name = '项目变更'
		verbose_name_plural = '项目变更列表'

	def __unicode__(self):
		return str(self.applicant)+'申请变更'\
		       +StatusProject.Remark(self.backward_status)\
		       +'为'+StatusProject.Remark(self.forward_status)



class ProjectRollbackApply(models.Model)	:
	applicant=models.ForeignKey(User,verbose_name='审核人',related_name='+',default=0)
	applicant_opinion= models.TextField(max_length=200, verbose_name='申请原因',default='')
	applicant_time=models.DateTimeField(verbose_name='申请时间',default=datetime.now, blank=True)

	project_apply=models.ForeignKey(ProjectApply, verbose_name='项目详情', related_name='+',default=0)
	project_name = models.CharField(verbose_name='项目名称', max_length=25,default='')
	project_type = models.ForeignKey(ProjectType, verbose_name='项目类型', related_name='+',default=0)
	project_no = models.CharField(verbose_name='项目代号', max_length=25,default='')
	project_status=models.IntegerField( verbose_name='项目状态',default=0)
	status = models.IntegerField( verbose_name='申请状态',default=0)
	unit=models.ForeignKey(Unit, verbose_name='所属单位', related_name='+',default=0)

	def save(self, force_insert=False, force_update=False, using=None):
		self.project_name = self.project_apply.project_name
		self.project_type = self.project_apply.project_type
		self.project_no = self.project_apply.project_no
		self.project_status=self.project_apply.status
		models.Model.save(self, force_insert, force_update, using)

	class Meta:
		verbose_name = '项目退回申请'
		verbose_name_plural = '项目退回申请列表'

	def __unicode__(self):
		return str(self.applicant)+'申请退回'+self.project_name

class ProjectRollbackApplyApprove(models.Model):
	approve=models.ForeignKey(User,verbose_name='单位名',related_name='+',default=0)
	approvetime = models.DateTimeField(verbose_name='审核时间',default=datetime.now, blank=True)
	approve_opinion = models.TextField(max_length=200, verbose_name='审核意见内容',default='')
	success = models.BooleanField(choices=((True, '同意'), (False, '不同意')), default=0)
	details=models.ForeignKey(ProjectRollbackApply,verbose_name='详情',related_name='+',default=0)

	class Meta:
		verbose_name = '项目退回申请审核'
		verbose_name_plural = '项目退回申请列表'

	def __unicode__(self):
		return self.approve.name+'审核'+str(self.details)

class ProjectExChangeApprove(models.Model):
	approve=models.ForeignKey(User,verbose_name='单位名',related_name='+',default=0)
	approvetime = models.DateTimeField(verbose_name='审核时间',default=datetime.now, blank=True)
	approve_opinion = models.TextField(max_length=200, verbose_name='审核意见内容',default='')
	success = models.BooleanField(choices=((True, '同意'), (False, '不同意')), default=0)
	details=models.ForeignKey(ProjectExChange,verbose_name='详情',related_name='+',default=0)

	class Meta:
		verbose_name = '项目变更申请审核'
		verbose_name_plural = '项目变更申请列表'

	def __unicode__(self):
		return self.approve.name+'审核'+str(self.details)


class LevelAchievement(models.Model):
	start_time=models.DateTimeField(verbose_name='开始时间',default=datetime.now, blank=True)
	end_time=models.DateTimeField(verbose_name='结束时间',default=datetime.now, blank=True)
	name=models.CharField(verbose_name='成果名称', max_length=200,default='')
	apply_user=models.CharField(verbose_name='承担人', max_length=25,default='')
	no=models.IntegerField(verbose_name='序号',default=0)
	apply=models.ForeignKey(ProjectApply,blank=True,null=True,default=0,related_name='level_achives')
	atype=models.CharField(verbose_name='成果形式', max_length=50,default='')
	class Meta:
		verbose_name = '主要阶段性成果'
		verbose_name_plural = '主要阶段性成果列表'


class FinalAchievement(models.Model):
	apply=models.ForeignKey(ProjectApply,blank=True,null=True,default=0,related_name='final_achives')

	end_time=models.DateTimeField(verbose_name='完成时间',default=datetime.now, blank=True)
	name=models.CharField(verbose_name='最终成果名称', max_length=200,default='')
	atype=models.CharField(verbose_name='成果形式', max_length=50,default='')
	font_num=models.IntegerField(verbose_name='统计字数',default=0)
	actor=models.CharField(verbose_name='参加人', max_length=50,default='')
	no=models.IntegerField(verbose_name='序号',default=0)

	class Meta:
		verbose_name = '最终成果'
		verbose_name_plural = '最终成果列表'

class ProjectActor(models.Model):
	apply=models.ForeignKey(ProjectApply,blank=True,null=True,default=0,related_name='actors')
	degree=models.CharField(verbose_name='学位', max_length=25,default='')
	name=models.CharField(verbose_name='姓名', max_length=25,default='')
	job_zw=models.CharField(verbose_name='职务', max_length=25,default='')
	job_zc=models.CharField(verbose_name='职称', max_length=25,default='')
	desc=models.TextField(max_length=200, verbose_name='近几年与本课题相关的研究成果',default='')

	class Meta:
		verbose_name = '项目参与者'
		verbose_name_plural = '项目参与者列表'


class ProjectApplyApprove(models.Model):
	approve=models.ForeignKey(User,verbose_name='审核人',related_name='+',default=0)
	approvetime = models.DateTimeField(verbose_name='审核时间',default=datetime.now, blank=True)
	approve_opinion = models.TextField(max_length=200, verbose_name='审核意见内容',default='')
	success = models.BooleanField(choices=((True, '同意'), (False, '不同意')), default=0)
	details=models.ForeignKey(ProjectApply,verbose_name='详情',related_name='+',default=0)
	expert_support=models.CharField(verbose_name='资助选项', max_length=50,default='')
	expert_percent=models.CharField(verbose_name='专家评分', max_length=50,default='')

	type=models.IntegerField( verbose_name='审批类型',default=0)


	class Meta:
		verbose_name = '项目申请审核'
		verbose_name_plural = '项目申请审核列表'

	def __unicode__(self):
		return str(self.approve)+'审核'+str(self.details)



class ProjectEndApply(models.Model):
	final_achieve_name=models.CharField(verbose_name='最终成果名称', max_length=200,default='')
	main_user_name=models.CharField(verbose_name='主要参加人', max_length=200,default='')
	achive_fomat=models.CharField(verbose_name='成果形式', max_length=50,default='')
	study_type_name=models.CharField(verbose_name='成果形式', max_length=50,default='')
	plain_end_time=models.DateTimeField(verbose_name='计划完成时间',default=datetime.now, blank=True)
	real_end_time=models.DateTimeField(verbose_name='实际完成时间',default=datetime.now, blank=True)
	font_num=models.CharField(verbose_name='字数', max_length=50,default='')
	unit_and_time=models.CharField(verbose_name='出版单位和时间', max_length=50,default='')
	go_where=models.CharField(verbose_name='字数', max_length=400,default='')
	final_desc=models.CharField(verbose_name='最终成果内容简介', max_length=600,default='')
	mingwei_option=models.CharField(verbose_name='国家民委教育科技司意见', max_length=600,default='')

	document=models.ForeignKey(Document, verbose_name='相关材料', related_name='+',default=0)
	file_code=models.CharField(verbose_name='文件编号', max_length=25,default='')
	project=models.ForeignKey(Project,verbose_name='项目ID',default=0)
	status=models.IntegerField( verbose_name='审批状态',default=0)
	applicant = models.ForeignKey(User, verbose_name='申请人', related_name='+',default=0)
	unit=models.ForeignKey(Unit,verbose_name='单位',related_name='+',default=0)

	class Meta:
		verbose_name = '项目结项审核'
		verbose_name_plural = '项目结项审核列表'

	def __unicode__(self):
		return self.final_achieve_name

class ProjectEndApplyApplicantAchieve(models.Model):
	name=models.CharField(verbose_name='最终成果名称', max_length=200,default='')
	unit_and_time=models.CharField(verbose_name='刊物年期、出版社和出版日期、使用单位', max_length=200,default='')
	desc=models.CharField(verbose_name='近几年与本课题相关的研究成果', max_length=200,default='')
	end_apply=models.ForeignKey(ProjectEndApply,verbose_name='结项申请',related_name='applicant_achieves',default=0)

	class Meta:
		verbose_name = '项目结项审核'
		verbose_name_plural = '项目结项审核列表'

	def __unicode__(self):
		return self.name

class ProjectEndApplyApprove(models.Model):
	approve=models.ForeignKey(User,verbose_name='审核人',related_name='+',default=0)
	approvetime = models.DateTimeField(verbose_name='审核时间',default=datetime.now, blank=True)
	approve_opinion = models.TextField(max_length=200, verbose_name='审核意见内容',default='')
	success = models.BooleanField(choices=((True, '同意'), (False, '不同意')), default=0)
	details=models.ForeignKey(ProjectEndApply,verbose_name='详情',related_name='+',default=0)

	class Meta:
		verbose_name = '项目结项审核'
		verbose_name_plural = '项目结项审核列表'

	def __unicode__(self):
		return self.approve.name+'结项审核'



class ConvertPDFTask(models.Model):
	documentid=models.IntegerField(verbose_name='文档ID',default=0)

	def Run(self,convet):
		document=Document.objects.get(pk=self.documentid)
		if document:
			pdf=document.pdf
			doc=document.doc
			if not os.path.exists(doc):
				document.converted=StatusConvert.NoExists
				print 'Word路径'+ doc+'未找到'
			else:
				try:
					convet(doc,pdf)
				except:
					document.converted_err=traceback.format_exc()
					document.converted=StatusConvert.Exception
					print doc+'转换异常'
				else:
					document.converted=StatusConvert.Success
					print doc+'转换成功'
			document.save()
		self.delete()

	class Meta:
		verbose_name = 'PDF转换任务'
		verbose_name_plural = 'PDF转换任务列表'

	def __unicode__(self):
		return str(self.documentid)

class ProjectApplyExpert(models.Model):
	expert=models.ForeignKey(User,verbose_name='专家', related_name='+',default=0)
	apply=models.ForeignKey(ProjectApply,verbose_name='项目申请', related_name='+',default=0)
	approved=models.BooleanField(choices=((True, '已审核'), (False, '未审核')), default=0)
	expert_support=models.CharField(verbose_name='资助选项', max_length=50,default='')
	expert_percent=models.CharField(verbose_name='专家评分', max_length=50,default='')

	#new
	refused=models.IntegerField(default=0,verbose_name='拒绝评审')
	email_back=models.IntegerField(default=0,verbose_name='邮件回执')
	email_key=models.CharField(default=Guid,verbose_name='邮件认证KEY',max_length=50)
	approvetime = models.DateTimeField(verbose_name='评审时间',default=datetime.now, blank=True)

Models = (
	ProjectEndApply,
	ProjectEndApplyApplicantAchieve,
	ProjectEndApplyApprove,
	Document,
        FinalAchievement,
        LevelAchievement,
        Message,
        Project,
        ProjectActor,
        ProjectApply,
        ProjectApplyApprove,
        ProjectExChange,
        ProjectExChangeApprove,
        ProjectType,
        Role,
        Unit,
        UnitLimitProjectType,
        User
)


