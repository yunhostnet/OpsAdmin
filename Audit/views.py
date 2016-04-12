#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from UserManage.views.permission import PermissionVerify

from UserManage.models import User
from Audit.models import Userlog

# Create your views here.

@login_required
@PermissionVerify()
def User_history(request):
    search = request.GET.get('keyword','')
    if search:
       lists = Userlog.objects.filter(username__contains=search) 
    else:
       lists = Userlog.objects.all().order_by('-date_added')
    lst = SelfPaginator(request,lists,20)
    kwvars = {'request':request,'lPage':lst}
    return render_to_response('Audit/user_history.html',kwvars,RequestContext(request))
