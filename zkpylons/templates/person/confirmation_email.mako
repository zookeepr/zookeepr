From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
Subject: ${ c.config.get('event_name') } Forgotten Password Reset Confirmation
To: ${ c.email }

%if c.person is not None:
To reset the password on the ${ c.config.get('event_name') } website account
for ${ c.email }, please click on the link below:

  ${ h.url_for(qualified=True, controller='person', action='reset_password', url_hash=c.conf_rec.url_hash) }

Please note that this URL will expire after 24 hours.

If you didn't ask for your password to be reset, you can ignore this
message as your password has not been changed yet.  The request will
expire in 24 hours.
%else:
Someone, possibly you, has requested a password reset on the ${ c.config.get('event_name') } 
website account.

However, you don't appear to have an account on the site. If you want to
sign up, please visit:

  ${ h.url_for(qualified=True, controller='person', action='new') }

If you didn't ask for your password to be reset, please ignore this
message.
%endif

The ${ c.config.get('event_name') } team
