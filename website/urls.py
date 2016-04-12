from django.conf.urls import patterns, include, url

from django.conf import settings
from website.views import *

#from django.contrib import admin
#admin.autodiscover()

handler404 = 'website.views.custom_Error_404'
handler500 = 'website.views.custom_Error_500'

urlpatterns = patterns('',
    #Examples:
    #url(r'^$', 'website.views.home', name='home'),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',Home),
    url(r'^index_cu/$',Index_cu,name='index_cu'),
    url(r'^file/upload/$',Fileupload,name='fileupload'),
    url(r'^file/download/$',Filedownload,name='filedownload'),
    url(r'^config/$',Global_config,name='config'),

    url(r'^accounts/',include('UserManage.urls')),
    url(r'^asset/',include('Asset.urls')),
    url(r'^authorize/',include('Authorize.urls')),
    url(r'^audit/',include('Audit.urls')),

    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}),
)
