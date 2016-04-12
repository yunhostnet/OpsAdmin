#!/usr/bin/env gg
#-*- coding: utf-8 -*-
#Auth:zp
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from UserManage.views.permission import PermissionVerify,Is_admin,Is_not_admin

from django.contrib import auth
from django.contrib.auth import get_user_model
from Asset.common import Hostupload,bash
from django.http import StreamingHttpResponse
from UserManage.models import User
from Asset.models import Asset
from Authorize.models import Authorize
from website.common.Api import to_days,get_count_num,Global_conf
from website.common.Confile_template import Config_File
from Asset.auto_get.host_api import BaseClass,File_download
from django.contrib.sessions.models import Session
from datetime import datetime

@login_required
@Is_admin()
def Home(request):
	lists_date,lists_str = to_days(7)
        lists_user = get_count_num(lists_date,T="user")
        lists_asset = get_count_num(lists_date,T="asset")
	user_count = User.objects.all()       
	host_conut = Asset.objects.all()
	authorize_count = Authorize.objects.all()
	online_sessison = Session.objects.filter(expire_date__gte=datetime.now())
        if not user_count:
	   user_count = 0
	if not host_conut:
	   host_conut = 0
	if not authorize_count:
           authorize_count = 0
	kwvars ={'request':request,'iuser':user_count,'ihost':host_conut,'iAuthorize':authorize_count,
		  'day':repr(lists_str),
		  'user_num':repr(lists_user),
		  'asset_num':repr(lists_asset),
		  'online':online_sessison.count(),
		}
	return render_to_response('index.html',kwvars,RequestContext(request))

@login_required
@Is_not_admin()
def Index_cu(request):
	kwvars ={'request':request}
	return render_to_response('index_cu.html',kwvars,RequestContext(request))

@login_required
@Is_not_admin()
def Fileupload(request):
    asset = Hostupload(request)
    if asset:
       kwvars ={'request':request,'assets':asset}
    else:
       kwvars ={'request':request}
    if request.method == 'POST':
       remote_ip = request.META.get('REMOTE_ADDR')
       asset_ids = request.POST.getlist('asset_ids', '')
       upload_files = request.FILES.getlist('file[]',None)
       count = 0
       upload_dir = "/tmp"
       uf = {}
       for upload_file in upload_files:
            file_path = '%s/%s' % (upload_dir, upload_file.name)
            with open(file_path, 'w') as f:
                for chunk in upload_file.chunks():
                    f.write(chunk)
		count += 1
	        uf["%s"%upload_file.name] = "%s"%file_path
       try:
	   re_li = []
           for i in asset_ids:
               a = Asset.objects.get(id = int(i))
               p = BaseClass(host=a.ip,user=a.username,passwd=a.password,port=int(a.port),cmd=None)
	       for k,v in uf.items():
		   file_name = k
                   rev = p.Localupload(file_name,s_path=v)
		   re_li.append(rev)
           msg = u'上传目录: %s  共%d个 成功%d个' % (upload_dir,len(upload_files),count)
           return HttpResponse(msg)
       except Exception,e:
	     error = "上传失败,请确认主机信息是否错误:%s"%(str(e))
	     return HttpResponse(error)
       #print re_li
    return render_to_response('upload.html',kwvars,RequestContext(request))    

@login_required
@Is_not_admin()
def Filedownload(request):
    asset = Hostupload(request)
    if asset:
       kwvars ={'request':request,'assets':asset}
    else:
       kwvars ={'request':request}
    if request.method=='POST':
       from os import path
       file_path = request.POST.get('file_path')
       assets = request.POST.getlist('assets', '')
       if not file_path or not assets:
	  kwvars['error'] ="文件路径和主机不能为空!"
          return render_to_response('download.html',kwvars,RequestContext(request))
       def file_iterator(file_name,chunk_size=512):
           with open(file_name) as f:
	        while True:
	              c = f.read(chunk_size)
		      if c:
			 yield c
	              else:
			 break
       #if path.exists(file_path):
       #if path.isfile(file_path):
       the_file_name = file_path
       file_name = the_file_name.split("/")[-1]
       local_path = "/tmp/%s"%file_name
       uf = []
       for i in assets:
           a = Asset.objects.get(id = int(i))
	   rev = File_download(a.ip,a.username,a.password,a.port,file_path,local_path)
           uf.append(rev)
       if uf:
	  if uf[0]:
          #if path.isdir(file_path):
          #   from time import time
	  #   random_num = time()
	  #   dir_name = file_path.split('/')[-1]
	  #   if(dir_name == ""):
          #      dir_name = file_path.split('/')[-2] 
	  #   file_name = "%s-%d.tar.gz"%(dir_name,random_num)
          #   bash("cd %s && tar czf /tmp/%s-%d.tar.gz *"%(file_path,dir_name,random_num))
          #   the_file_name = "/tmp/%s"%(file_name)
       #else:
         #kwvars['error'] ="咱不支持目录下载!"
         #return render_to_response('download.html',kwvars,RequestContext(request))
             response = StreamingHttpResponse(file_iterator(local_path))
             response['Content-Type'] = 'application/octet-stream'
             response['Content-Disposition'] = 'attachment;filename=%s'%(path.basename(file_name))
             return response
          else:
             kwvars['error'] = u"下载失败,请查看日志!"
       else:
      	 kwvars['error'] = u"下载失败!"
    return render_to_response('download.html',kwvars,RequestContext(request))

@login_required
@Is_admin()
def Global_config(request):
    conn = Global_conf(request.META['WORKING_DIR'])
    db_info = conn.reload_db()
    ldap_info = conn.reload_ldap()
    kwvars ={'request':request,'db':db_info,'ldap':ldap_info}
    if request.method=='POST':
       db_name = request.POST.get('db_name')
       db_ip = request.POST.get('db_ip')
       db_user = request.POST.get('db_user')
       db_pass = request.POST.get('db_pass')
       db_port = request.POST.get('db_port')

       ldap_host = request.POST.get('ldap_host')
       ldap_user = request.POST.get('ldap_user')
       ldap_pass = request.POST.get('ldap_pass')
       ldap_status = request.POST.get('ldap_status')
       ldap_base = request.POST.get('ldap_base')
       db_dicts = {'db_ip':db_ip,'db_name':db_name,'db_pass':db_pass,'db_user':db_user,'db_port':db_port}
       ldap_dicts = {'ldap_host':ldap_host,'ldap_user':ldap_user,'ldap_pass':ldap_pass,
		     'ldap_status':ldap_status,'ldap_base':ldap_base}
       ret = Config_File(request.META['WORKING_DIR'],db_dicts,ldap_dicts)
       if ret:
	  kwvars['msg'] = "修改成功!"
       else:
	  kwvars['err'] = "修改失败"
    return render_to_response('config.html',kwvars,RequestContext(request))

def custom_Error_404(request):
	return render_to_response('404.html')
def custom_Error_500(request):
	return render_to_response('500.html')
