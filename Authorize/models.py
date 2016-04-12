#!/usr/bin/env python
# Create your models here.
from django.db import models
from Asset.models import Asset,AssetGroup
from UserManage.models import User

class Authorize(models.Model):
    name = models.CharField(max_length=100, unique=True)
    asset = models.ManyToManyField(Asset,related_name='auth_rule')
    asset_group = models.ManyToManyField(AssetGroup,related_name='auth_rule')
    user = models.ManyToManyField(User,related_name='auth_rule')
    date_added = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
