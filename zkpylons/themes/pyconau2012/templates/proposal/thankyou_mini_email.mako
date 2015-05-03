From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your ${ c.proposal.type.name.lower() } proposal for ${ c.config.get('event_name') }

Dear ${ c.person.firstname },

Thank you for proposing a ${ c.proposal.type.name.lower() } for ${ c.config.get('event_name') }.

If you have any queries about your proposed ${ c.proposal.type.name.lower() }, please email
${ c.proposal.type.notify_email.lower() }

Title:       ${ c.proposal.title }
URL:         ${ c.proposal.url }
Attachments: ${ len(c.proposal.attachments) }
Summary:     ${ c.proposal.abstract }

Should you need to update the details of this proposal, please use the following
URL:

  http://${ c.config.get('event_host') }/proposal


The ${ c.config.get('event_name') } team
http://${ c.config.get('event_host') }/contact
