#!/usr/bin/env python
#coding:utf8
#from website.common.Api import get_object

from django import template
from Authorize.common import get_asset_count,get_assetgroup_count,get_asset_host
from UserManage.views.permission import More_per

register = template.Library()

@register.filter(name='intostr')
def intostr(value):
    return str(value)
@register.filter(name='hostgroup_str')
def hostgroup_str(group_list):
    if len(group_list) < 2:
        return ';'.join([group.name for group in group_list])
    else:
        return '%s ..' % ';'.join([group.name for group in group_list[0:2]])

@register.filter(name='hostgroup_strd')
def hostgroup_strd(group_list):
    if len(group_list) < 8:
       return ';'.join([group.name for group in group_list])
    else:
       return '%s ...' % ';'.join([group.name for group in group_list[0:2]])

@register.filter(name='boolstr')
def boolstr(value):
    if value:
        return u'是'
    else:
        return u'否'
@register.filter(name='member_count')
def member_count(instance,member):
    member = getattr(instance, member)
    counts = member.all().count()
    return str(counts)

@register.filter(name='asset_num')
def asset_num(uid):
    us = get_asset_count(uid)
    if us:
	return us
    else:
        return 0

@register.filter(name='asset_group_num')
def asset_group_num(uid):
    user = get_assetgroup_count(uid)
    if user:
       return user
    else:
       return 0

@register.filter(name='asset_host_all')
def asset_host_all(uid):
    u = get_asset_host(uid)
    if u:
       if len(u) < 8:
          return ' , '.join([i for i in u])
       else:
          return '%s ...' % ' , '.join([i for i in u[0:7]])
    else:
       return u"无"

@register.filter(name='more_per')
def more_per(uid):
    if uid:
       role_list = More_per(uid)
       return role_list
