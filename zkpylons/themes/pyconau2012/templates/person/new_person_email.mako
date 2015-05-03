Subject: ${ c.config.get('event_name') } New Account Confirmation
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>

Dear ${ c.person.firstname },

Thank you for creating a login to the ${ c.config.get('event_name') } website.
Please validate your account by clicking on this URL:

  ${ h.url_for(qualified=True, controller='person', action='confirm', confirm_hash=c.person.url_hash) }

Once your account has been confirmed, you will be able to log into the web
site with the password you provided.

Thanks and have a great day!

The ${ c.config.get('event_name') } team
