From: ${ h.lca_info['event_name'] } <${ h.lca_info['contact_email'] }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your ${ c.proposal.type.name.lower() } proposal for ${ h.lca_info['event_name'] }

Dear ${ c.person.firstname },

Thank you for proposing a ${ c.proposal.type.name.lower() } for ${ h.lca_info['event_name'] }.

If you have any queries about your proposed ${ c.proposal.type.name.lower() }, please email
${ h.lca_info['emails'][c.proposal.type.name.lower()] }

Title:       ${ c.proposal.title }
URL:         ${ c.proposal.url }
Attachments: ${ len(c.proposal.attachments) }
Summary:     ${ c.proposal.abstract }

Should you need to update the details of this proposal, please following
this URL:

  http://${ h.host_name() }/proposal


The ${ h.event_name() } team
http://${ h.host_name() }/contact
