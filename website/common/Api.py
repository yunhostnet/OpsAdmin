#!/usr/bin/env python
#Auth:zp
#Created:2016.02.05
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime,timedelta,date
from Audit.models import Userlog
from Asset.models import Asset
from ConfigParser import ConfigParser

def get_object(model,**kwargs):
    for value in kwargs.values():
        if not value:
            return None
    objects = model.objects.filter(**kwargs)
    if len(objects) == 1:
        objects = objects[0]
    else:
        objects = None
    return objects

def render_to(template, data, request):
    return render_to_response(template,data,context_instance=RequestContext(request))

def to_days(num):
   #lists = []
   #now = datetime.now().strftime("%m-%d")
   #for i in range(1,8):
   #    begin = (date.today() - timedelta(days=i)).strftime("%m-%d")
   #    lists.append(begin)
   #return lists[::-1]
   #today = datetime.utcnow().replace(tzinfo = utc).date()
   today = date.today()
   oneday = timedelta(days=1)
   date_li, date_str = [], []
   for i in range(0, num):
        today = today-oneday
        date_li.append(today)
        date_str.append(str(today)[5:10])
   date_li.reverse()
   date_str.reverse()
   return date_li, date_str

def get_count_num(date_li,T=None):
    lists = []
    if(T=="user"):
       for start in date_li:
           end = start + timedelta(days=1)
           lists_num = Userlog.objects.filter(date_added__range=(start,end))
           lists.append(len(lists_num))
    if(T=="asset"):
      for start in date_li:
	  end = start + timedelta(days=1)
	  lists_num = Asset.objects.filter(date_added__range=(start,end))
	  lists.append(len(lists_num))
    return lists

class Global_conf(object):
    def __init__(self,workdir):
       config = ConfigParser()
       config.read('%s/opsadmin.cfg'%(workdir))
       self.DB_HOST = config.get('db','host')
       self.DB_PORT = config.getint('db','port')
       self.DB_USER = config.get('db','user')
       self.DB_PASSWD   = config.get('db','passwd')
       self.DB_DATABASE = config.get('db','database')

       self.LDAP_HOST = config.get('ldap','ldap_host')
       self.LDAP_DN = config.get('ldap','ldap_bind_dn')
       self.LDAP_PASS = config.get('ldap','ldap_bind_passwd')
       self.LDAP_STATUS = config.get('ldap','ldap_status')
       self.LDAP_BASE = config.get('ldap','ldap_base')
    def reload_db(self):
	db_dict = {'db_ip':self.DB_HOST,'db_user':self.DB_USER,'db_pass':self.DB_PASSWD,
		   'db_port':self.DB_PORT,'db_name':self.DB_DATABASE}
	return db_dict
    def reload_ldap(self):
	ldap_dict = {'ldap_host':self.LDAP_HOST,'ldap_user':self.LDAP_DN,
	             'ldap_pass':self.LDAP_PASS,'ldap_status':self.LDAP_STATUS,
		     'ldap_base':self.LDAP_BASE}
	return ldap_dict

