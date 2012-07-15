From: ${ h.lca_info['event_name'] } <${ h.lca_info['contact_email'] }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your ${ c.funding.type.name } funding request for ${ h.lca_info['event_name'] }

Dear ${ c.person.firstname },

Thank you for submitting a ${ c.funding.type.name } requestfor ${ h.lca_info['event_name'] }.

If you have any queries about your funding request ${ c.funding.type.name },
please email ${ c.funding.type.notify_email }

Should you need to update the details of this request, please use the following
URL:

  http://${ h.host_name() }/funding


The ${ h.event_name() } team
http://${ h.host_name() }/contact
