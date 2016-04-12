#!/usr/bin/env python

from django import forms
from jasset.models import Asset,AssetGroup

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            "ip","hostname","port", "hostgroup", "username", "password", "use_default_auth",
            "mac", "remote_ip", "brand", "cpu", "memory", "disk", "system_type",
            "cabinet", "position", "number", "status", "asset_type", "env", "sn","comment"]
