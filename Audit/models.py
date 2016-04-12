#!/usr/bin/env python
#coding:utf8
from django.db import models

# Create your models here.

class Userlog(models.Model):
    username = models.CharField(max_length=128,verbose_name=u"用户名")
    remote_ip = models.CharField(max_length=32,blank=True,null=True, verbose_name=u"登陆IP地址")
    session_key = models.CharField(max_length=40)
    date_added = models.DateTimeField(auto_now=True,null=True)
    logout_added = models.DateTimeField(null=True)
    expire_added = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return self.remote_ip
