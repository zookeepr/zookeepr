From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your ${ c.funding.type.name } funding request for ${ c.config.get('event_name') }

Dear ${ c.person.firstname },

Thank you for submitting a ${ c.funding.type.name } requestfor ${ c.config.get('event_name') }.

If you have any queries about your funding request ${ c.funding.type.name },
please email ${ c.funding.type.notify_email }

Should you need to update the details of this request, please use the following
URL:

  http://${ c.config.get('event_host') }/funding


The ${ c.config.get('event_name') } team
http://${ c.config.get('event_host') }/contact
