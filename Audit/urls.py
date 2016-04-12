from django.conf.urls import patterns,include,url
from Audit.views import *

urlpatterns = patterns('Audit.views',
	# Examples:
	url(r'^user/history/$',User_history,name='user_history'),
)
