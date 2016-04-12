#!/usr/bin/env python
#coding:utf8
#Auth:zp
#Created:2016.02.05

from Authorize.models import Authorize

def get_asset_count(uid):
    try:
        user = Authorize.objects.get(user = uid).asset.count()
        return user
    except:
	return False
def get_assetgroup_count(uid):
    try:
        user = Authorize.objects.get(user = uid).asset_group.count()
        return user
    except:
	return False
def get_asset_host(uid):
    try:
       user = Authorize.objects.get(user = uid).asset.all()
       user_list = [str(i) for i in user]
       return user_list
    except:
       return False
