#!/usr/bin/env python
#coding:utf8
#Auth:zp
#Version 1.0.0
import paramiko
import time
import threading
from os import path

def write_log(basedir,host,stderr):
	f = open("%s/logs/all.log"%basedir,'a+')
	tm=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	log = ("[%s] %s  %s \n"%(tm,host,stderr))
	f.write(log)
	f.close()

def File_download(host,user,passwd,port,remote_file,local_file):
     basedir = path.abspath(path.dirname(__file__))
     try:
	ssh = paramiko.Transport((host,int(port)))
	ssh.connect(username=user,password=passwd)
	sftp = paramiko.SFTPClient.from_transport(ssh)
	sftp.get(remote_file,local_file)
	sftp.close()
	ssh.close()
	return True
     except Exception,e:
        write_log(basedir,host,e)
	return False

class BaseClass(threading.Thread):
	def __init__(self,host,user,passwd,port,cmd):
	    threading.Thread.__init__(self)
	    self.basedir = path.abspath(path.dirname(__file__))
	    self.host = host
	    self.user = user
	    self.passwd = passwd
	    self.port = port 
	    self.cmd = cmd
        def run(self,cmdd):
	    try:
		#key=paramiko.RSAKey.from_private_key_file(sshkey_file)
		#ssh.load_system_host_keys()
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.host,int(self.port),self.user,self.passwd,timeout=1)
		stdin,stdout,stderr = ssh.exec_command(cmdd)
		rev = stdout.read()
		err = stderr.read()
		if err:
		   print err
		   write_log(self.basedir,self.host,err)
	        ssh.close()
	        return rev
	    except Exception,e:
		print "%s"%(str(e))
                write_log(self.basedir,self.host,e)
	        ssh.close()
            
        def Localupload(self,file_name,s_path,d_path="/tmp"):
	    try:
	        ssh = paramiko.Transport((self.host,int(self.port)))
		ssh.connect(username = self.user,password = self.passwd)
		sftp = paramiko.SFTPClient.from_transport(ssh)
		ret = sftp.put(s_path,"%s/%s"%(d_path,file_name))
		if ret:
                    sftp.close()
	            ssh.close()
	            return True
	    except Exception,e:
                write_log(self.basedir,self.host,e)
                sftp.close()
	        ssh.close()
		return False

def Get_Process(host,user,passwd,port,cmd):
        p = BaseClass(host,user,passwd,port,cmd)
	file_path = cmd.split()[1]
	if path.exists(file_path):
           if path.isfile(file_path):
	       file_name = file_path.split("/")[-1]
	       s = p.Localupload(file_name,file_path)
	       cmdd = "%s /tmp/%s"%(cmd.split()[0],file_name)
	       if s:
                  return p.run(cmdd)
           if path.isdir(file_path):
	      err = "必须是文件"
	      write_log(basedir,host,err)
	else:
	   err = "文件不存在"
           write_log(basedir,host,err)
	   return 0
	#p.setDaemon(True)
        #return p.run()

#command = "bash /tmp/all_info.sh"
#print Get_Process(host='118.244.173.254',user='root',passwd='200888chang',port='22',cmd=command)
