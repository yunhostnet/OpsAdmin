#!/usr/bin/env python
#coding:utf8
from django.db import models

# Create your models here.
HOST_TYPE = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"容器"),
    )
class AssetGroup(models.Model):
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)
    def __unicode__(self):
        return self.name

class Asset(models.Model):
    hostname = models.CharField(unique=True, max_length=128, verbose_name=u"主机名")
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"IP地址")
    #hostgroup = models.ForeignKey(AssetGroup, blank=True, verbose_name=u"主机组")
    port = models.IntegerField(blank=True, null=True, verbose_name=u"端口号")
    username = models.CharField(max_length=16, blank=True, null=True, verbose_name=u"管理用户")
    password = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"管理密码")
    hostgroup = models.ManyToManyField(AssetGroup, blank=True, verbose_name=u"主机组")
    use_default_auth = models.BooleanField(default=True, verbose_name=u"使用默认管理账号")
    mac = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"MAC地址")
    remote_ip = models.CharField(max_length=16, blank=True, null=True, verbose_name=u'远控卡IP')
    brand = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'硬件厂商型号')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    disk = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'硬盘')
    system_type = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"系统信息")
    cabinet = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'机柜号')
    position = models.IntegerField(blank=True, null=True,verbose_name=u'机器位置')
    #position = models.CharField(blank=True, null=True,verbose_name=u'机器位置')
    number = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'资产编号')
    asset_type = models.IntegerField(choices=HOST_TYPE, blank=True, null=True, verbose_name=u"主机类型")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"SN编号")
    date_added = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(default=True, verbose_name=u"是否开启")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.ip
