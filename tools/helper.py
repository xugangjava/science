#coding=utf-8

import datetime
from email.header import Header
from email.mime.text import MIMEText
import os
import smtplib
import uuid
import comtypes
from django.forms import forms
from django.http import Http404, HttpResponse
# Get an instance of a logger
import time
from django.utils.encoding import smart_unicode
from tools.const import Const

def CallBack(msg):
	return {'success':True,'msg':msg}

OK= {'success':True,'msg':'OK'}

def ErrCallBack(msg='Error'):
	return {'success':False,'msg':msg}

def IntVal(x,default=0):
	if not x:return default
	if not str(x).isdigit():return default
	return int(x)

def CurPage(total,items):
	return {'total':total,'items':items}

def Items(value):
	return {'items':list(value)}

def StartLimit(request):
	start=request.POST.get('start')
	limit=request.POST.get('limit')
	if not start:start=request.GET.get('start')
	if not limit:limit=request.GET.get('limit')
	start,limit= IntVal(start,0),IntVal(limit,20)

	return start,start+limit



def GetParam(reques,*params):

	kv={}
	for p in params:
		if reques.GET.has_key(p):
			kv[p]=smart_unicode(reques.GET[p])
		elif reques.POST.has_key(p):
			kv[p]=smart_unicode(reques.POST[p])
		else:
			print 'baseParam '+str(p)+ ' lost '
			raise Http404
	return kv

def GetArrayParams(reques,*params):
	kv={}
	#分组param
	group_kv={}

	def filliparam(k,v):
		if k.startswith('g__'):
			arry=k.split('__')
			gname,attr,index=arry[1],arry[2],arry[3]
			if not gname in group_kv:
				group_kv[gname]={}
			if not index in group_kv[gname]:
				group_kv[gname][index]={}

			group_kv[gname][index][attr]=smart_unicode(v,strings_only=True)
		else:
			kv[k]=smart_unicode(v,strings_only=True)

	def checkparam(p):
		if p.startswith('g__'):
			arry=p.split('__')
			gname,attr=arry[1],arry[2]
			for g in group_kv[gname].values():
				if not attr in g:
					print 'groupParam '+p+' is lost\n'
					raise Http404
		else:

			if not p in kv:
				print 'baseParam '+p+' is lost\n'
				raise Http404


	for k,v in  reques.GET.iteritems():
		filliparam(k,v)

	for k,v in  reques.POST.iteritems():
		filliparam(k,v)

	for p in params:
		checkparam(p)


	return kv,group_kv

def YMD(date):
	return str(date.year)+"年"+str(date.month)+"月"+str(date.day)+"日"

def IdArray(ids):
	if any(not i.isdigit() for i in ids.split(',')):
		raise Http404
	return [int(i)  for i in ids.split(',')]


def FillModel(kv, object, exclude=None):
	if not exclude: exclude = []
	for k,v in kv.iteritems():
		if k in exclude:continue
		if Const.DEBUG:print 'now run set filed '+k
		if not v:return ErrCallBack('缺少参数'+k)
		if not hasattr(object,k):return ErrCallBack('属性名错误'+k)
		value,attr=v,getattr(object,k)
		if isinstance(attr,int):
			value=int(value)
		elif isinstance(attr,datetime.datetime):
			value= datetime.datetime.fromtimestamp(time.mktime(time.strptime(value,u"%Y年%m月%d日")))

		setattr(object,k,value)
		if Const.DEBUG:print 'finished set filed '+k
	return object

class TryGetParamResult:
	def __init__(self):
		self.value=None

	def __nonzero__(self):
		return self.value is not None

	def __init__(self):
		self.value=None


def TryGetParam(request,key):
	r=TryGetParamResult()
	if request.GET.has_key(key):
		r.value=request.GET.get(key)
	elif request.POST.has_key(key):
		r.value=request.POST.get(key)
	return r

def FileExt(filename):
	return os.path.splitext(filename)[-1].lower()

def GuidFileName(filename):
	return Guid()+FileExt(filename)

def Str2DateTime(string):
	string=string.decode('utf-8')
	return datetime.datetime.fromtimestamp(time.mktime(time.strptime(string,u"%Y年%m月%d日")))


def Guid():
	return str(uuid.uuid4()).replace('-','')


def Sex(val):
	return '男' if val else '女'

def TimeNow():
	return time.strftime('%Y年%m月%d日',time.localtime(time.time()))



def RawDoc(filecode):
	code=Const.HERE+'/media/project/'+filecode
	print code
	print code+'.doc'
	print code+'.docx'
	if os.path.exists(code+'.doc'):
		code += '.doc'
	elif os.path.exists(code+'.docx'):
		code += '.docx'
	else:
		code=None
	return code


def EmailNotify(to_users,message):
	me="<sysnotify@163.com>"
	msg = MIMEText(message)
	msg['Subject'] = '市科技局审核系统提示'
	try:
		s = smtplib.SMTP()
		s.connect('smtp.163.com')
		s.login('sysnotify','123456aA')
		for u in to_users:
			s.sendmail(me,u.email, msg.as_string())
		s.close()
		return True
	except Exception, e:
		if Const.DEBUG:print str(e)
		return False

class ExcelRender:
	def __init__(self,title,key,render=None):
		self.title=title
		self.render=render
		self.key=key

import xlwt
def WriteDictToExcel(kvarray,renders):


	response = HttpResponse(mimetype="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=document.xls'
	wb = xlwt.Workbook(encoding = 'utf-8')
	ws = wb.add_sheet('data')
	x=0
	for r in renders:
		print r.title
		ws.write(0,x,r.title)
		x+=1
	y=1
	for kv in kvarray:
		x=0
		for r in renders:
			v=kv[r.key]
			if r.render:v=r.render(v)
			ws.write(y,x,v)
			x+=1
		y+=1
	wb.save(response)
	return response





#excel convert pdf file
if __name__=='__main__':
	Const.HERE=r'F:\Quick\Projects'
	print RawDoc('b4b4b96cac1b4eb984f411ed42758e7c')


#	me="<sysnotify@163.com>"
#	msg = MIMEText('just a test 市科技局审核系统提示','plain', 'utf-8')
#	msg['Subject'] =Header('市科技局审核系统提示', 'utf-8')
#
#	s = smtplib.SMTP()
#	s.connect('smtp.163.com')
#	s.login('sysnotify','123456aA')
#	s.sendmail(me,'<xugangjava@163.com>',smart_unicode(msg.as_string()) )
#	s.close()
#	Doc2Pdf(r'F:\Quick\Projects\science\media\project\ffe6bf32cff04873a21d2bda24bea281.docx'
#		,r'F:\Quick\Projects\science\media\project\ffe6bf32cff04873a21d2bda24bea281.pdf')




#		w.Quit(constants.wdDoNotSaveChanges)

##powerpoint convert pdf file
#def ppt2pdf(input,output):
#	p = Dispatch("PowerPoint.Application")
#	p.Visible = True
#	try:
#		print input
#		pptFile = p.Presentations.Open(input)
#		print 'open ppt successful!'
#		pptFile.SaveAs(output)
#		#pptFile.ExportAsFixedFormat(output,17)
#		print 'powerpoint file convert successful!'
#		return 0
#	except:
#		print 'powerpoint file convert failed!'
#		return 1
#	finally:
#		p.Quit()
#


