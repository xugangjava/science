#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from science import settings

admin.autodiscover()



urlpatterns = patterns('',
	url(r'static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.STATIC_ROOT+'/ext/'}),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

)

#core
urlpatterns += patterns('',
        url(r'^login/$','core.views.login'),
	url(r'^loginout/$','django.contrib.auth.views.logout',{'next_page': '/'}),


	url(r'^main/$','core.views.main'),
	url(r'^register/user/$','core.views.register_user'),
	url(r'^register/unit/$','core.views.register_unit'),
 	url(r'^login/code/$','core.views.raw_code'),

)


#user
urlpatterns+=patterns('',
	url('^user/add/$','core.views.user_add'),
	url('^user/list/$','core.views.user_list'),
	url('^user/del/$','core.views.user_del'),
	url('^user/update/$','core.views.user_update'),
	url('^user/selfupdate/$','core.views.user_self_update'),
	url('^user/details/$','core.views.user_detail'),
	url('^user/approve/$','core.views.user_approve'),
	url('^user/list/approve/$','core.views.user_list_approve'),

	url('^user/name/$','core.views.user_name'),
	url('^expert/set/', 'core.views.expert_set'),
	url('^expert/combo/$','core.views.expert_combo'),

	url('^user/notify/count/$','core.views.admin_notify_count'),
)

#role
urlpatterns+=patterns('',
	url('^role/combo/$','core.views.role_combo')
)

#unit
urlpatterns+=patterns('',
	url('^unit/combo/$','core.views.unit_combo'),

	url('^unit/list/approve/$','core.views.unit_list_approve'),
	url('^unit/list/$','core.views.unit_list'),
	url('^unit/add/$','core.views.unit_add'),
	url('^unit/details/$','core.views.unit_details'),
	url('^unit/del/$','core.views.unit_del'),
	url('^unit/update/$','core.views.unit_update'),
	url('^unit/approve/$','core.views.unit_approve')
)

#project
urlpatterns+=patterns('',
	url('^projecttype/list/$','core.views.project_type_list'),
	url('^projecttype/combo/$','core.views.projecttype_combo'),
	url('^project/list/$','core.views.project_list'),
	url('^project/search/$','core.views.project_search'),
	url('^project/count/$','core.views.project_count'),

	url('^projecttype/details/$','core.views.project_type_details'),
	url('^projecttype/update/$','core.views.project_type_update'),


	url('^project/rollback/add/$','core.views.project_rollback_add'),
	url('^project/rollback/list/$','core.views.project_rollback_list'),
	url('^project/rollback/approve/$','core.views.project_rollback_approve'),


	url('^project/end/add/$','core.views.project_end_add'),
	url('^project/end/list/$','core.views.project_end_list'),
	url('^project/end/approve/$','core.views.project_end_approve'),

	url('^project/exchange/add/$','core.views.project_exchange_add'),
	url('^project/exchange/list/$','core.views.project_exchange_list'),
	url('^project/exchange/approve/$','core.views.project_exchange_approve'),


	url('^projectapply/add/$', 'core.views.project_apply_add'),
	url('^project/apply/list/$','core.views.project_apply_list'),
	url('^project/apply/approve/$','core.views.project_apply_approve'),
	url('^project/apply/submit/$','core.views.project_apply_submit'),
	url('^project/apply/details/$','core.views.project_apply_details'),

	#project_apply_details
	url('^project/apply/showdetails/$','core.views.project_apply_show_details'),
	url('^project/show/details/$','core.views.project_show_details'),

	#show approves
	url('^project/apply/approves/$', 'core.views.project_apply_all_approves'),
	url('^project/end/approves/$', 'core.views.project_end_all_approves'),
	url('^project/back/approves/$', 'core.views.project_back_all_approves'),
	url('^project/exchange/approves/$', 'core.views.project_exchange_all_approves'),

	#show admin approves
	url('^project/admin/apply/approves/$', 'core.views.project_admin_apply_all_approves'),
	url('^project/admin/end/approves/$', 'core.views.project_admin_end_all_approves'),
	url('^project/admin/back/approves/$', 'core.views.project_admin_back_all_approves'),
	url('^project/admin/exchange/approves/$', 'core.views.project_admin_exchange_all_approves'),
)


#message
urlpatterns+=patterns('',
	url('^message/list/$','core.views.message_list'),
	url('^message/waitpublist/$','core.views.mesage_waitpublist'),
	url('^message/add/$','core.views.message_add'),
	url('^message/notify/$','core.views.message_notify'),
	url('^message/pub/$','core.views.message_pub'),
	url('^message/show/details/','core.views.message_details'),
	url('^message/message_recvier_combo/$','core.views.message_recvier_combo'),
	url('^message/sended/list/$','core.views.message_sended_list')
)

#document
urlpatterns+=patterns('',
#	url('^raw/doc/(?P<url>.*)$', 'core.views.raw_doc'),
#	url('^open/project/apply/doc/(?P<pk>\d+)/$','core.views.raw_project_apply_doc'),
#
#	url('^raw/pdf/(?P<url>.*)$','core.views.raw_pdf'),
#	url('^open/project/apply/pdf/(?P<pk>\d+)/$','core.views.raw_project_apply_pdf')
	url('^document/download/(?P<pk>\d+)/$', 'core.views.download_document'),
	url('^project/apply/pdf/download/(?P<pk>\d+)/$', 'core.views.download_project_apply_pdf'),
	url('^project/admin/project/done/xls/export/$','core.views.download_project_admin_apply_all_approves_excel'),
	url('^project/apply/doc/upload/$', 'core.views.upload_project_apply_doc'),
	url('^temp/project_apply/doc/$', 'core.views.download_project_apply_doc_temp'),
)


urlpatterns+= patterns('django.views.generic.simple',
        url(r'^$','direct_to_template', {'template':'login/login.htm'}),
	url('^document/$','direct_to_template', {'template':'word.html'}),
)


