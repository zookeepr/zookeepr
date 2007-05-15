import smtplib
from zookeepr.lib.base import *

def email(recipients, body):
    try:
	s = smtplib.SMTP(
	    request.environ['paste.config']['global_conf'].get('smtp_server'))
	s.sendmail(
            request.environ['paste.config']['app_conf'].get('contact_email'),
            recipients, body)
	s.quit()
    except:
	pass

