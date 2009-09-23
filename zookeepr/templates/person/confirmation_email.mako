From: ${ h.lca_info['event_name'] } <${ h.lca_info['contact_email'] }>
Subject: ${ h.event_name() } Forgotten Password Reset Confirmation
To: ${ c.email }

%if c.person is not None:
To reset the password on the ${ h.event_name() } website account
for ${ c.email }, please click on the link below:

  ${ h.lca_info['event_url'] }${ h.url_for(controller='person', action='reset_password', url_hash=c.conf_rec.url_hash) }

Please note that this URL will expire after 24 hours.

If you didn't ask for your password to be reset, you can ignore this
message as your password has not been changed yet.  The request will
expire in 24 hours.
%else:
Someone, possibly you, has requested a password reset on the ${ h.event_name() } 
website account.

However, you don't appear to have an account on the site. If you want to
sign up, please visit:

  ${ h.lca_info['event_url'] }${ h.url_for(controller='person', action='new') }

If you didn't ask for your password to be reset, please ignore this
message.
%endif

The ${ h.event_name() } team
