#coding=utf-8
import datetime
import decimal

from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.utils.timezone import is_aware
from django.db import models
from science import settings
from const import Const

from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads
from django.db.models.query import QuerySet, ValuesQuerySet
from django.utils.functional import curry


class DjangoJSONEncoder(simplejson.JSONEncoder):
	"""
		JSONEncoder subclass that knows how to encode date/time and decimal types.
	"""
	def default(self, o):
		# See "Date Time String Format" in the ECMA-262 specification.
		if isinstance(o, datetime.datetime):
			return o.strftime('%Y年%m月%d日')
		elif isinstance(o, datetime.date):
			return o.isoformat()
		elif isinstance(o, datetime.time):
			if is_aware(o):
				raise ValueError("JSON can't represent timezone-aware times.")
			r = o.isoformat()
			if o.microsecond:
				r = r[:12]
			return r
		elif isinstance(o, decimal.Decimal):
			return str(o)
		elif isinstance(o,ValuesQuerySet):
			return list(o)
		elif isinstance(o, QuerySet):
			return loads(serialize('json', o))
		elif isinstance(o, models.Model):
			return dict([(attr, getattr(o, attr)) for attr in [f.name for f in o._meta.fields]])
		else:
			return super(DjangoJSONEncoder, self).default(o)


dumps = curry(dumps, cls=DjangoJSONEncoder)

def Ajax(fn):
	def wrapper(*args, **kv):
		request = args[0]
		if not  settings.DEBUG and\
		not request.is_ajax():
			raise Http404
		result= fn(*args, **kv)
		result=dumps(result)
		return HttpResponse(result,mimetype="application/json")
	return wrapper


def AjaxXML(fn):
	def wrapper(*args, **kv):
		request = args[0]
		if not  settings.DEBUG and\
		   not request.is_ajax():
			raise Http404
		result= fn(*args, **kv)
		return HttpResponse(result,mimetype="application/xml")
	return wrapper


def Auth(request,*arg):
	if not Const.User in  request.session:raise Http404
	user= request.session[Const.User]
	if not user:raise Http404
	if not arg:return user
	for code in arg:
		if code and code==user.role.code:
			return user
	raise Http404

def Users(fn):
	def wrapper(*args, **kv):
		user=args[0].session[Const.User]
		if not user:raise Http404
		return fn(*args, **kv)
	return wrapper

def Expert(fn):
	def wrapper(*args, **kv):
		Auth(args[0],Const.EXPERT)
		return fn(*args, **kv)
	return wrapper

def Admin(fn):
	def wrapper(*args, **kv):
		Auth(args[0],Const.ADMIN)
		return fn(*args, **kv)
	return wrapper

def Applicant(fn):
	def wrapper(*args, **kv):
		Auth(args[0],Const.APPLICANT)
		return fn(*args, **kv)
	return wrapper








