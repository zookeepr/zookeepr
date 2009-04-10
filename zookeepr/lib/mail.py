import smtplib
from zookeepr.lib.base import *
from zookeepr.config.lca_info import lca_info

def email(recipients, body):
    try:
        if type(recipients) in (str, unicode):
            recipients = [recipients, lca_info['bcc_email']]
        else:
            recipients += [lca_info['bcc_email']]

        s = smtplib.SMTP(
                request.environ['paste.config']['global_conf'].get('smtp_server'))
        s.sendmail(
            lca_info['contact_email'],
            recipients, body)
        s.quit()
    except:
        raise

