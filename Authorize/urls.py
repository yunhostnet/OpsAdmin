from django.conf.urls import patterns, include, url
from Authorize.views import *

urlpatterns = patterns('Authorize.views',
	# Examples:
	url(r'^authorize_list/$',Authorize_list,name='authorize_list'),
	url(r'^authorize_add/$',Authorize_add,name='authorize_add'),
	url(r'^authorize_edit/(?P<ID>\d+)/$',Authorize_edit,name='authorize_edit'),
	url(r'^authorize_del/(?P<ID>\d+)/$',Authorize_del,name='authorize_del'),
)
