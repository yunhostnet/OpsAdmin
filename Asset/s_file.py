#!/usr/bin/env python

from auto_get.host_api import Get_Process


all_list = []
command = "bash /home/work/project/opsadmin/Asset/auto_get/all_info.sh"
all_info = Get_Process(host='127.0.0.1',user='root',passwd="200888chang",port=60205,cmd=command)
for i in all_info.strip('\n').split(','):
	all_list.append(i)
for i in all_list:
	key = i.split(';')[0]
	if(key=="disk_info"):
	    s = i.replace(" ","")
	    k = s.split(';')[0]
	    v = s.split(';')[1]
	    print k
	    print v
	         
	else:	
	    v = i.split(';')[1]

