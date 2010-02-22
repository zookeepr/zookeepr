Subject: ${ h.event_name() } New Account Confirmation
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>

Dear ${ c.person.firstname },

Thank you for creating a login to the ${ h.event_name() } website.
Please validate your account by clicking on this URL:

  ${ h.lca_info['event_url'] }${ h.url_for('acct_confirm', confirm_hash=c.person.url_hash) }

Once your account has been confirmed, you will be able to log into the web
site with the password you provided.

Don't forget to sign up to our announcements mailing list via

  http://lists.linux.org.au/listinfo/lca-announce

Thanks and have a great day!

The ${ h.event_name() } team
