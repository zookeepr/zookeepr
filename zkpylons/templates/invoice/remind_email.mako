From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
To: ${ c.recipient.firstname } ${ c.recipient.lastname } <${ c.recipient.email_address }>
Subject: You haven't paid for your ${ c.config.get('event_name') } registration

Dear ${ c.recipient.firstname },

This is a reminder that you haven't paid for your ${ c.config.get('event_name') }
registration.

You can view your registration and pay your outstanding invoice at 
${ h.url_for(qualified=True, controller='registration', action='status', id=None) }

If you have recieved this email and already paid your invoice please reply with
further information.

Regards,

The ${ c.config.get('event_name') } team
