From: ${ h.lca_info['event_name'] } <${ h.lca_info['contact_email'] }>
To: ${ c.recipient.firstname } ${ c.recipient.lastname } <${ c.recipient.email_address }>
Subject: You haven't paid for your ${ h.lca_info['event_name'] } registration

Dear ${ c.recipient.firstname },

This is a reminder that you haven't paid for your ${ h.lca_info['event_name'] }
registration. Earlybird tickets are almost sold out and will not be
available after midnight AEST tomorrow.

You can view your registration and pay your outstanding invoice at 
${ h.url_for(qualified=True, controller='registration', action='status', id=None) }

If you have paid for your invoice, and you think you're receiving this in error,
please reply to this email with further information.

Regards,

The ${ h.lca_info['event_name'] } team
