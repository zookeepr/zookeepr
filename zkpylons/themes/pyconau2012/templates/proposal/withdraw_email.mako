From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
To: ${ c.email_address }
Subject: WITHDRAWAL of a ${ c.proposal.type.name.lower() } proposal

${c.person.firstname} ${c.person.lastname} has withdrawn the following proposal:

Title:             ${ c.proposal.title }
Target audience:   ${ c.proposal.audience.name }
Summary:           ${ c.proposal.abstract }
