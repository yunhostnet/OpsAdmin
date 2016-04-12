#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from UserManage.views.permission import PermissionVerify

from UserManage.models import User
from Asset.models import Asset,AssetGroup
from Authorize.models import Authorize
# Create your views here.

@login_required
@PermissionVerify()
def Authorize_list(request):
    lists = Authorize.objects.all()
    lst = SelfPaginator(request,lists,20)
    kwvars = {'request':request,'lPage':lst}
    return render_to_response('Authorize/authorize_list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def Authorize_add(request):
    users = User.objects.all()
    assets = Asset.objects.all()
    assetgroups = AssetGroup.objects.all()
    kwvars = {'request':request,'users':users,'assets':assets,'assetgroups':assetgroups}
    if request.method=='POST':
	    name = request.POST.get('name')
	    user_select = request.POST.getlist('user',[])
	    asset_select = request.POST.getlist('asset',[])
	    assetgroup = request.POST.getlist('asset_group',[])
	    comment= request.POST.get('comment')
	    
	    assets_select = [Asset.objects.get(id=asset) for asset in asset_select]
	    assets_group = [AssetGroup.objects.get(id=gid) for gid in assetgroup]
	    group_assets = []
	    for i in assets_group:
		    group_assets.extend(list(i.asset_set.all()))
	    calc = set(group_assets) | set(asset_select)

	    users = [User.objects.get(id=uid) for uid in user_select]

            a = Authorize(name=name,comment=comment)
            a.save()
            a.user = users
            a.asset = assets_select
            a.asset_group = assets_group
            a.save()
	    return HttpResponseRedirect(reverse('authorize_list'))
    return render_to_response('Authorize/authorize_add.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def Authorize_edit(request,ID):
    users = User.objects.all()
    assets = Asset.objects.all()
    assetgroups = AssetGroup.objects.all()
    auth = Authorize.objects.get(id = ID)
    kwvars = {'request':request,'users':users,'assets':assets,'assetgroups':assetgroups,'auth':auth}
    if request.method=='POST':
	    name = request.POST.get('name')
	    user_select = request.POST.getlist('user',[])
	    asset_select = request.POST.getlist('asset',[])
	    assetgroup = request.POST.getlist('asset_group',[])
	    comment= request.POST.get('comment')
	    assets_select = [Asset.objects.get(id=asset) for asset in asset_select]
	    assets_group = [AssetGroup.objects.get(id=gid) for gid in assetgroup]
	    users = [User.objects.get(id=uid) for uid in user_select]

	    auth.name = name
	    auth.comment = comment
	    auth.save()
            auth.user = users
	    auth.asset = assets_select
	    auth.asset_group = assets_group
	    auth.save()
	    return HttpResponseRedirect(reverse('authorize_list')) 
    return render_to_response('Authorize/authorize_edit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def Authorize_del(request,ID):
      a = Authorize.objects.get(id = ID)
      a.delete()
      return HttpResponseRedirect(reverse('authorize_list'))
