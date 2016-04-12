#!/usr/bin/env python
#coding:utf8
#Auth:jason.zp
#Created:2016.02.22

from Audit.models import Userlog

def Login_re(request):
     try:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                IP =  request.META['HTTP_X_FORWARDED_FOR']
        else:
                IP = request.META['REMOTE_ADDR']
        a = Userlog()
	a.username  = request.user.username
	a.remote_ip = IP
	a.save()
     except Exception,e:
	return "%s"%e
