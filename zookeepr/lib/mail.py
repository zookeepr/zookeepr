import smtplib

#from zookeepr.lib.base import *
from zookeepr.config.lca_info import lca_info
from pylons import config

def email(recipients, body):
    try:
        s = smtplib.SMTP(config['smtp_server'])
        s.sendmail(
            lca_info['contact_email'],
            recipients, body)
        s.quit()
    except:
        raise

