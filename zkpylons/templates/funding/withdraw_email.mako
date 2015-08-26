From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
To: ${ c.email_address }
Subject: WITHDRAWAL of a ${ c.funding.type.name } proposal

${c.person.firstname} ${c.person.lastname} has withdrawn their funding
request for a ${ c.funding.type.name }.
