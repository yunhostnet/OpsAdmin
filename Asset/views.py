#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from website.common.Api import render_to
from UserManage.views.permission import PermissionVerify,Is_not_admin

from Asset.models import Asset,AssetGroup,HOST_TYPE
from Authorize.models import Authorize
from Asset.common import add_group,update_group,host_update,update_host
from Asset.common import Hostpermission,write_excel,write_excel_db
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
@PermissionVerify()
def Alist(request):
    search = request.GET.get('keyword','') 
    export = request.GET.get('export','')
    kwvars = {'request':request,'asset_type':HOST_TYPE,'URL':'alist'}
    if(len(search)!=0):
        lists = Asset.objects.filter(hostname__contains=search)
    else:
    	lists = Asset.objects.all()
    if export:
       try:
          rev = write_excel(lists,user=request.user.username)
	  return rev
       except Exception,e:
         kwvars["err"] = "导出列表错误!%s"%(str(e))
         return render_to_response('status.html',kwvars,RequestContext(request))

    lst = SelfPaginator(request,lists,20)
    kwvars['lPage'] = lst
    return render_to_response('Asset/asset_list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def Hostlist(request,ID):
    search = request.GET.get('keyword','')
    if(len(search)!=0):
      lists = Authorize.objects.get(user = ID).asset.filter(hostname__contains=search) 
    else:
      lists = Authorize.objects.get(user = ID).asset.all()
    lst = SelfPaginator(request,lists,20)
    kwvars = {'request':request,'lPage':lst,'asset_type':HOST_TYPE}
    return render_to_response('Asset/asset_list.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Grouplist(request,ID):
    host_list = Asset.objects.all()
    lists = Authorize.objects.get(user = ID).asset_group.all()
    lst = SelfPaginator(request,lists,20)
    kwvars = {'request':request,'lPage':lst,'host_list':host_list}
    return render_to_response('Asset/asset_group_list.html',kwvars,RequestContext(request))

@login_required
@Is_not_admin()
def Userhost(request):
    kwvars = {'URL':'user_host_list','request':request,'asset_type':HOST_TYPE}
    search = request.GET.get('keyword','')
    export = request.GET.get('export','')
    uid = get_user_model().objects.get(username = request.user.username)
    if(len(search)!=0):
      lists = Authorize.objects.get(user = uid.id).asset.filter(hostname__contains=search) 
    else:
      try:
         lists = Authorize.objects.get(user = uid.id).asset.all()
      except Exception,e:
	 kwvars["err"] = "没有授权主机%s"%(str(e))
	 return render_to_response('status.html',kwvars,RequestContext(request))
    if export:
       try:
          rev = write_excel(lists,user=request.user.username)
	  return rev
       except Exception,e:
         kwvars["err"] = "导出列表错误!%s"%(str(e))
         return render_to_response('status.html',kwvars,RequestContext(request))
    lst = SelfPaginator(request,lists,20)
    kwvars['lPage'] = lst
    return render_to_response('Asset/user_host_list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def Glist(request):
    lists = AssetGroup.objects.all() 
    host_list = Asset.objects.all()
    lst = SelfPaginator(request,lists,20)
    kwvars = {'lPage':lst,'host_list':host_list,'request':request}
    return render_to_response('Asset/asset_group_list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def Aadd(request):
    kwvars = {'asset_type':HOST_TYPE,'request':request}
    if request.method=='POST':
	    hostname = request.POST.get('hostname')
	    ip = request.POST.get('ip')
	    username = request.POST.get('user')
	    password = request.POST.get('passwd')
	    port = request.POST.get('port')
	    asset_type = request.POST.get('asset_type')
	    status_id = request.POST.get('status')
	    lists = Asset.objects.filter(hostname = hostname)
	    if len(lists) == 0:
		  a = Asset()
                  a.hostname = hostname
		  a.ip = ip
		  a.username = username
		  a.password = password
		  a.port = port
		  a.asset_type = asset_type
		  if(status_id=='0'):a.status = False
		  a.save()
                  return HttpResponseRedirect(reverse('alist'))
            else: 
		  kwvars['err'] = "%s已存在!"%(str(hostname))
    return render_to_response('Asset/asset_add.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Batch_add(request):
    kwvars = {'request':request}
    if request.method == 'POST':
       excel_file = request.FILES.get('file_name','')
       try:
          ret = write_excel_db(excel_file)
	  if ret[0]:
	     kwvars['msg'] = "导入成功!"
	  else:
             kwvars['err'] = "导入失败!%s"%(ret[1])
       except Exception,e:
	  kwvars['err'] = "导入失败!%s"%(str(e))
    return render_to('Asset/asset_add_batch.html',kwvars,request)

@login_required
@PermissionVerify()
def Gadd(request):
    kwvars = {'URL':'glist','request':request}
    if request.method=='POST':
	    name = request.POST.get('groupname')
	    host_select = request.POST.getlist('host_select',[])
	    comment = request.POST.get('comment')
            lists = AssetGroup.objects.filter(name = name)
	    if len(lists) == 0:
		    add_group(name=name,comment=comment,host_select=host_select)
		    kwvars['msg'] = "添加成功!"
		    return render_to_response('status.html',kwvars,RequestContext(request))
            else:
		    kwvars['err'] = "%s已存在!"%(str(name))
		    return render_to_response('status.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Aedit(request,ID):
    a = Asset.objects.get(id = ID)
    kwvars = {'request':request,'URL':'alist','host':a,'asset_type':HOST_TYPE}
    if request.method=='POST':
	    hostname = request.POST.get('hostname')
	    ip = request.POST.get('ip')
	    port = request.POST.get('port')
	    username = request.POST.get('username')
	    passwd = request.POST.get('passwd')
	    remote_ip = request.POST.get('remote_ip')
	    brand = request.POST.get('brand')
	    cabinet = request.POST.get('cabinet')
	    position = request.POST.get('position')
	    number = request.POST.get('number')
	    sn = request.POST.get('sn')
	    comment = request.POST.get('comment')
	    ass=update_host(a,hostname,ip,port,username,passwd,remote_ip,brand,cabinet,position,number,sn,comment)
	    if(ass=="ok"):
              kwvars['msg'] = "修改成功!"
	      return render_to_response('status.html',kwvars,RequestContext(request))
            else:
	      kwvars['err'] = "修改失败!,%s"%(ass)
	      return render_to_response('status.html',kwvars,RequestContext(request))
    return render_to_response('Asset/asset_edit.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Gedit(request,ID):
      group = AssetGroup.objects.filter(id = ID)
      if len(group) == 1:
	  group = group[0]
      else:
	  group = None
      host_list = Asset.objects.all()
      host_select = Asset.objects.filter(hostgroup = group)
      host_no_select = [i for i in host_list if i not in host_select]
      kwvars = {'request':request,'URL':'glist','host_select':host_select,'host_no_select':host_no_select,'group':group}
      if request.method=='POST':
	  name = request.POST.get('groupname')
	  host_select = request.POST.getlist('host_select',[])
	  comment = request.POST.get('comment')
          group.asset_set.clear()
          #lists = AssetGroup.objects.filter(name = name)
	  try:
	     update_group(id=ID,name=name,host_select=host_select,comment=comment)
	     kwvars['msg'] = "修改成功!"
	     return render_to_response('status.html',kwvars,RequestContext(request))
          except Exception,e:
             kwvars['err'] = "修改出错%s!"%(str(e))
	     return render_to_response('status.html',kwvars,RequestContext(request))
      return render_to_response('Asset/asset_group_edit.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Gdel(request,ID):
    kwvars = {'request':request,'URL':'glist'}
    try:
        AssetGroup.objects.filter(id = ID).delete()
        kwvars['msg'] = "删除成功!"
	return render_to_response('status.html',kwvars,RequestContext(request))
    except:
	kwvars['err'] = "删除失败!"
	return render_to_response('status.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Mdel(request):
	kwvars = {'request':request,'URL':'alist'}
        Id = request.GET.get('ids')
        ids = Id.split(',')
        try:
                for i in ids:
                        Asset.objects.filter(id = i).delete()
		kwvars['msg'] = "删除成功!"
		return render_to_response('status.html',kwvars,RequestContext(request))
        except Exception,e:
		kwvars['err'] = "删除失败!"
		return render_to_response('status.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
def Mddel(request,ID):
      Asset.objects.filter(id = ID).delete()
      return HttpResponseRedirect(reverse('alist'))

@csrf_exempt
@login_required
@PermissionVerify()
def Host_update(request):
    if request.method == 'POST':
       Id = unicode(request.POST.get('ids',''))
       for ids in Id.split(','):
	   sta = Asset.objects.get(id = ids)
           if(sta.status == False):
	     return HttpResponse(u'[%s]主机已被禁用!'%(sta.ip))     
       rcev = host_update(Id)
       if(rcev != "ok"):
          return HttpResponse(u'更新失败,请查看日志!')
       else:
          return HttpResponse(u'更新成功!')

@login_required
@Hostpermission()
def Host_details(request,ID):
    all_info = Asset.objects.get(id = ID)
    kwvars = {'request':request,'host':all_info,'asset_type':HOST_TYPE}
    return render_to_response('Asset/asset_details.html',kwvars,RequestContext(request))

@login_required
def Status_check(request):
    ids = unicode(request.GET.get('ids',''))
    if ids == "status":
       return HttpResponse("down")
    else:
       return HttpResponse("错误")
