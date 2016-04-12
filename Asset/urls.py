from django.conf.urls import patterns, include, url
from Asset.views import *

urlpatterns = patterns('Asset.views',
	# Examples:
	url(r'^list/$',Alist,name='alist'),
	url(r'^host/list/(?P<ID>\d+)/$',Hostlist,name='host_list'),
	url(r'^group/list/(?P<ID>\d+)/$',Grouplist,name='group_list'),
	
	url(r'^add/$',Aadd,name='aadd'),
	url(r'^batch/add/$',Batch_add,name='batch_add'),
	url(r'^edit/(?P<ID>\d+)/$',Aedit,name='aedit'),
	url(r'^mdel/$',Mdel,name='mdel'),
	url(r'^mddel/(?P<ID>\d+)/$',Mddel,name='mddel'),
	url(r'^details/(?P<ID>\d+)/$',Host_details,name='host_details'),
	url(r'^host/update/$',Host_update,name='host_update'),

	url(r'^glist/$',Glist,name='glist'),
	url(r'^gadd/$',Gadd,name='gadd'),
	url(r'^gedit/(?P<ID>\d+)/$',Gedit,name='gedit'),
	url(r'^gdel/(?P<ID>\d+)/$',Gdel,name='gdel'),

	url(r'^user/host/list/$',Userhost,name='user_host_list'),

	url(r'^status/check/$',Status_check,name='status_check'),
)
