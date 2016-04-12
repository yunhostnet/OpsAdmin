#!/usr/bin/python
#coding:utf8
#-------------------------------------------------------------------------------
# Author:      zp
# Copyright:   2016.01.26
#-------------------------------------------------------------------------------
import smtplib
import string
from email.mime.text import MIMEText

def sender(subject,content,format='plain'):
	Mail_Server = 'mail.iyunxiao.com'
	FROM = 'zoupeng@iyunxiao.com'
	PASS = '123.com..'
	TOS = []
	for i in TO:
		TOS.append(i)
	SUBJECT = subject
	TEXT = content
	
	msg = MIMEText(TEXT,format,'utf-8')
	msg["Subject"] = SUBJECT
	msg["TO"] = TO 
	msg["Accept-Language"]="zh-CN"
	msg["Accept-Charset"]="ISO-8859-1,utf-8"
	try:
		server = smtplib.SMTP(timeout=1)
		server.connect(Mail_Server,"465")
		server.starttls()
		server.login(FROM,PASS)
		server.sendmail(FROM,TOS,msg.as_string())
		return(0,"+OK:mail from %s send %s success."%(FROM,TO))
	except smtplib.SMTPAuthenticationError as e:
		return(1,"Error:username or passwd match error.Info:%s"%(str(e)))
	except smtplib.SMTPServerDisconnected as e:
		return(1,"Error:network anomaly.Info:%s"%(str(e)))
	except Exception,e:
		return(1,"Error:mail to send failure.Info:%s"%(str(e)))
	server.quit()
