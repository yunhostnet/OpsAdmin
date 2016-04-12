#!/usr/bin/env python
#config file template
#Created:2016.03.04

def Config_File(workdir,db_dicts,ldap_dicts):
    try:
       db = db_dicts
       ldap = ldap_dicts
       f = open("%s/opsadmin.cfg"%(workdir),"w+")
       conf_file = '''#This is opsadmin configure file.
[db]
host = %s
port = %s     
user = %s     
passwd = %s   
database = %s      
                   
[ldap]             
#0 False or 1 Ture Need Restart APP
ldap_status = %s   
ldap_host = %s     
ldap_bind_dn = %s  
ldap_bind_passwd = %s
ldap_base = %s '''%(db['db_ip'],db['db_port'],db['db_user'],db['db_pass'],db['db_name'],
       ldap['ldap_status'],ldap['ldap_host'],ldap['ldap_user'],ldap['ldap_pass'],ldap['ldap_base']
       )
       f.write(conf_file)
       f.close()
       return True
    except:
       return False
