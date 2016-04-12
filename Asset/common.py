#!/usr/bin/env python
#coding:utf8
from django.core.urlresolvers import reverse
from Asset.models import Asset,AssetGroup
from django.core.paginator import Paginator
from auto_get.host_api import Get_Process
from Authorize.models import Authorize
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from os import getcwd,listdir,remove
from subprocess import call
from xlrd import open_workbook
from datetime import datetime,timedelta
from django.http import StreamingHttpResponse
from website.common.Api import get_object
import xlsxwriter
from UserManage.views.permission import More_per

def Hostpermission():
    def decorator(view_func):
        def _wrapped_view(request,*args,**kwargs):
	    ids = kwargs.get('ID')
	    if request.user.username != "admin":
	       if request.user.role_id:
		  lists = More_per(request.user.role_id)
		  ts = False
		  for i in lists:
		      if(i.url.split("/")[1] == "asset"):
                          ts = True
		  if not ts:
		     return HttpResponseRedirect(reverse('permissiondenyurl'))
               else:
	           uid = get_user_model().objects.get(username = request.user.username)
	           lists = Authorize.objects.get(user = uid.id).asset.all().filter(id=ids)
                   if not lists:
                      return HttpResponseRedirect(reverse('permissiondenyurl'))
            return view_func(request,*args,**kwargs)
        return _wrapped_view
    return decorator

def Hostupload(request):
    try:
       uid = get_user_model().objects.get(username = request.user.username)
       lists = Authorize.objects.get(user = uid.id).asset.all()
       return lists
    except Exception,e:
      return False

def bash(cmd):
    return call(cmd, shell=True)

def add_group(**kwargs):
    name = kwargs.get('name')
    group = AssetGroup.objects.filter(name=name)
    asset_list = kwargs.pop('host_select')
   
    if not group:
        hostgroup = AssetGroup(**kwargs)
        hostgroup.save()
        for ids in asset_list:
		lst = Asset.objects.filter( id = ids )
		if lst:
		   hostgroup.asset_set.add(lst[0])
def update_group(**kwargs):
    group_id = kwargs.pop('id')
    host_id_list = kwargs.pop('host_select')
    group = AssetGroup.objects.filter( id=group_id)
    if len(group) == 1:
           group = group[0]
    else:
           group = None
    for ids in host_id_list:
         lst = Asset.objects.filter( id = ids )
         if lst:
            group.asset_set.add(lst[0])
    AssetGroup.objects.filter(id=group_id).update(**kwargs)

def host_update(Id):
    try:
       all_list = []
       all_dict = {}
       for ids in Id.split(','):
           isa = Asset.objects.get(id = ids)
           command = "bash %s/Asset/auto_get/all_info.sh"%(getcwd())
           all_info = Get_Process(host=isa.ip,user=isa.username,passwd=isa.password,port=int(isa.port),cmd=command)
           for i in all_info.strip('\n').split(','):
	       all_list.append(i)
           for c in all_list:
	        key = c.split(';')[0]
	        value = c.split(';')[1]
		if(key=="disk_info"):
			s = c.replace(" ","")
			value = s.split(';')[1]
	        all_dict[key] = value
           isa.cpu = "%s核"%(all_dict["cpu_info"])
           isa.memory = "%dG"%(int(all_dict["mem_info"])/1024/1024)
           isa.disk = all_dict["disk_info"]
           isa.system_type = all_dict["system"]
           isa.mac = all_dict["mac"]
           isa.save()
       return "ok"
    except Exception,e:
       return "%s"%(str(e))

def update_host(a,hostname,ip,port,username,passwd,remote_ip,brand,cabinet,position,number,sn,comment):
    try:
       a.hostname = hostname
       a.ip = ip
       a.username = username
       a.password = passwd
       a.remote_ip = remote_ip
       a.brand = brand
       a.cabinet = cabinet
       if(position==""):
	       position = 0
       a.position = position
       a.number = number
       a.sn = sn
       a.comment = comment
       a.save()
       return "ok"
    except Exception,e:
       return "%s"%(str(e))

def write_excel(lists,user,T=None):
    data = []
    files = "static/files"
    his_rm = [ remove("%s/%s"%(files,i)) for i in listdir(files) ]
    
    now_date = datetime.now().strftime('%Y_%m_%d_%H_%M')
    if(T=="user"):
      file_name = user + '_user_excel_' + now_date + '.xlsx'
      workbook = xlsxwriter.Workbook('%s/%s'%(files,file_name))
      worksheet = workbook.add_worksheet(u'用户数据')
    else:
      file_name = user + '_cmdb_excel_' + now_date + '.xlsx'
      workbook = xlsxwriter.Workbook('%s/%s'%(files,file_name))
      worksheet = workbook.add_worksheet(u'CMDB数据')
    worksheet.set_first_sheet()
    worksheet.set_column('A:E', 15)
    worksheet.set_column('F:F', 40)
    worksheet.set_column('G:Z', 15)
    if(T=="user"):
      title = [u'登陆名', u'用户名', u'性别', u'手机号', u'QQ号', u'邮箱', u'状态',u'最后一次登陆时间']
      for u in lists:
          #last_login = u.last_login + timedelta(hours=8) #setting.py USER_TZ = True 
          dicts = [u.username,u.nickname,u.sex,u.moblie_num,u.qq_num,u.email,u.is_active,str(u.last_login)]
          data.append(dicts)
    else:
      title = [u'主机名称', u'IP地址', u'所属主机组', u'操作系统', u'CPU', u'内存(G)', u'硬盘(G)',
             u'机柜位置', u'MAC', u'远控IP', u'机器状态', u'备注']
      for asset in lists:
        group_list = []
        for p in asset.hostgroup.all():
            group_list.append(p.name)
        group_all = '/'.join(group_list)
        system_type = asset.system_type if asset.system_type else u''

        dicts = [asset.hostname, asset.ip, group_all, system_type, asset.cpu, asset.memory,
                asset.disk, asset.cabinet, asset.mac, asset.remote_ip, asset.status, asset.comment]
        data.append(dicts)

    format = workbook.add_format()
    format.set_border(1)
    format.set_align('center')
    format.set_align('vcenter')
    format.set_text_wrap()

    format_title = workbook.add_format()
    format_title.set_border(1)
    format_title.set_bg_color('#cccccc')
    format_title.set_align('center')
    format_title.set_bold()

    format_ave = workbook.add_format()
    format_ave.set_border(1)
    format_ave.set_num_format('0.00')

    worksheet.write_row('A1', title, format_title)
    i = 2
    for alter in data:
        location = 'A' + str(i)
        worksheet.write_row(location, alter, format)
        i += 1

    workbook.close()
    rev = (True,file_name)
    if rev[0]:
       ret = StreamingHttpResponse(file_iterator('%s/%s'%(files,rev[1])))
       ret['Content-Type'] = 'application/octet-stream'
       ret['Content-Disposition'] = 'attachment;filename=%s'%(rev[1])
       return ret

def write_excel_db(excel_file):
    try:
        data = open_workbook(filename=None,file_contents=excel_file.read())
    except Exception,e:
        return (False,str(e))
    else:
        table = data.sheets()[0]
        rows = table.nrows
        for row_num in range(1,rows):
            row_data = table.row_values(row_num)
            if row_data:
#                group_instance = []
                name,ip,system,cpu,memory,disk,mac,asset_type,remote_ip,brand,cabinet,position,number,sn,status,comment = row_data
                if get_object(Asset,hostname=name):
                    continue
#                use_default_auth = 1 if use_default_auth == u'默认' else 0
#                password_encode = CRYPTOR.encrypt(password) if password else ''
		if not position:
	           position = 0
                if name:
                    a = Asset(ip=ip,
                                  hostname = name,
				  mac = mac,
				  remote_ip = remote_ip,
				  cpu = cpu,
				  memory = memory,
			          disk = disk,
				  system_type = system,
				  asset_type = asset_type,
				  brand = brand,
				  cabinet = cabinet,
				  position = position,
				  number = number,
				  sn = sn,
				  status = status,
				  comment = comment
                             )
                    a.save()
#                    group_list = group.split('/')
#                    for group_name in group_list:
#                        group = get_object(AssetGroup, name=group_name)
#                        if group:
#                            group_instance.append(group)
#                    if group_instance:
#                        asset.group = group_instance
#                    asset.save()
        return (True,1)

def file_iterator(file_name,chunk_size=512):
    with open(file_name) as f:
         while True:
             v = f.read(chunk_size)
             if v:
                yield v
             else:
                break 
