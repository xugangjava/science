#coding=utf-8
import ImageFont

class Const:
	User='SESSION_USER'
	OK='OK'
	FAIL='FAIL'

	ADMIN='admin'
	EXPERT='expert'
	APPLICANT='applicant'

	HERE=''
	DEBUG=False
	CODE_FONT=None

	@staticmethod
	def ProjectRoot():
		return Const.HERE+'/media'

	@staticmethod
	def CodeFont():
		if not Const.CODE_FONT:
			Const.CODE_FONT=ImageFont.truetype(Const.HERE+'/msyh.ttf',14)
		return Const.CODE_FONT

def IsAdmin(user):
	return user.role.code==Const.ADMIN

def IsSysAdmin(user):
	return IsAdmin(user) and user.unit.level==0


def IsApplicant(user):
	return user.role.code==Const.APPLICANT

def IsExpert(user):
	return user.role.code==Const.EXPERT

class StatusUnit:
	APPROVE=-1
	NORMAL=0
	APPROVE_FAIL=-2

class StatusUser:
	APPROVE=-1
	NORMAL=0
	APPROVE_FAIL=-2


ApproveStatus = {
	0:'失败',
	1: '通过',
	-4: '等待市科技局审核',
	-3: '等待专家评审',
	-5: '等待推送专家评审',
	-2: '等待二级管理员审核',
	-1: '等待一级管理员审核',
	-8: '市科技局管理员退回',
	-6: '二级单位管理员退回',
	-7: '一级单位管理员退回',
        -9:'等待提交',
        -10:'待国家民委审查'
}


class StatusApprove:

	WAIT_EXPERT=-3
	WAIT_SET_EXPERT=-5
	WAIT_ADMIN_0=-4
	WAIT_ADMIN_2=-2
	WAIT_ADMIN_1=-1
	WAIT_SUBMIT=-9
	WAIT_AMIDN_0_LOOK=-10
	SUCCESS=1

	FAILED_ADMIN_0=-8
	FAILED_ADMIN_2=-6
	FAILED_ADMIN_1=-7

	@staticmethod
	def Remark(value):
		return ApproveStatus.get(value,'未知状态')


ProjectStatus={
	-7:'退回',
	-6:'延期',
	-5:'撤项',
	  0:'正常',
          1:'结项'
}

class StatusProject:
	BACK=-7
	LAZY=-6
	UNDO=-5
	NORMAL=0
	DONE=1
	@staticmethod
	def Remark(value):
		return ProjectStatus.get(value,'未知状态')


UnitLevel={
	0:'国家民委',
	1:'一级单位',
	2:'二级单位',
	3:'三级单位',
	4:'四级单位',
	5:'五级单位',
	6:'六级单位',
	7:'七级单位',
	8:'八级单位',
}
class StatusConvert:
	Success=1
	Wati=0
	Exception=-1
	NoExists=-2

ConvertStatus={
	  1:'转换pdf成功',
	  0:'待转换',
	-1:'转换pdf异常',
	-2:'word文档不存在'
}

ProjectArea={
	u"人文社会科学": 'S',
	u"自然科学": 'Z',
	u"文理交叉": 'C',
	u"其他": 'O'
}

UnitNo={
	u'中央民族大学':'ZY',
        u'中南民族大学':'ZN',
        u'西北民族大学':'XB',
        u'北方民族大学':'BF',
        u'广西民族大学':'GX',
        u'西南民族大学':'XN',
        u'云南民族大学':'YN'
}




class DisableCSRF(object):
	def process_request(self, request): setattr(request, '_dont_enforce_csrf_checks', True)
