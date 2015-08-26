import email.header as email_header
import email.parser as email_parser
import email.utils as email_utils
import smtplib
import string
import traceback

import zkpylons.lib.helpers as h
from zkpylons.model.config import Config
from pylons import config

def is_7bit(s):
    return not s.lstrip(string.printable)

def encode_header(s):
    tailed = s.rstrip(string.printable)
    topped = tailed.lstrip(string.printable)
    encoded = email_header.Header(topped, 'utf-8').encode()
    front = s[:len(tailed) - len(topped)]
    back_len = len(s) - len(tailed)
    back = "" if back_len == 0 else s[-back_len:]
    return front + encoded + back

def encode_addr(addr):
    email_desc, email_addr = email_utils.parseaddr(addr)
    if not is_7bit(email_desc):
        email_desc = encode_header(email_desc)
    return email_utils.formataddr((email_desc, email_addr))

email_addr_headers = (
        'bcc',
        'cc',
        'from',
        'reply-to',
        'resend-cc',
        'resend-to',
        'resent-from',
        'sender',
        'to',
    )

recipient_addr_headers = (
        'cc',
        'resend-cc',
        'resend-to',
        'to',
    )

def email(recipients, body):
    message = email_parser.Parser().parsestr(body.encode('utf-8'))
    addrs = []
    # Get rid of 8-bit chars in the email address fields.
    for addr_header in email_addr_headers:
        addrs = message.get_all(addr_header)
        if not addrs or is_7bit(', '.join(addrs)):
            continue
        del message[addr_header]
        encoded_addrs = ', '.join([encode_addr(a) for a in addrs])
        message[addr_header] = encoded_addrs
    # Get rid of 8-bit chars in the other message headers.
    for header_name in set(message.keys()):
        headers = message.get_all(header_name)
        if is_7bit(''.join(headers)):
            continue
        del message[header_name]
        for utf_header in headers:
            if is_7bit(''.join(headers)):
                ascii_header = utf_header
            else:
                ascii_header = encode_header(utf_header)
            message[header_name] = ascii_header
    # If the body isn't plain ascii, encode it as well.
    if not message.get_charset():
        email_body = message.get_payload()
        if not is_7bit(email_body):
            message.set_charset('utf-8')
    # Default the recipients to the 'To', etc headers in the email.
    if not recipients:
        addrs = []
        for recipient_header in recipient_addr_headers:
            addrs.extend(message.get_all(recipient_header, []))
        addrs = email_utils.getaddresses(addrs)
        recipients = [email_utils.formataddr(a) for a in addrs]
    elif type(recipients) in (str, unicode):
        recipients = [recipients]
    #
    # If bcc_email is set, send it there as well.
    #
    if Config.get('bcc_email'):
        recipients.append(Config.get('bcc_email'))
    # send the email using smtp
    try:
        s = smtplib.SMTP(config['smtp_server'])
        s.sendmail(Config.get('contact_email'), recipients, message.as_string())
        s.quit()
    except Exception as e:
        h.flash(
            'Unable to send email. '
            'Please contact %s' % Config.get('webmaster_email'),
            'error'
        )
        traceback.print_exc()
