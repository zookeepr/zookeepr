Subject: ${ h.event_name() } Proposal Offer Confirmation
To: ${ c.person.fullname() } <${ c.person.email_address }>

Dear ${ c.person.firstname },

%if c.status.name == 'Accepted':
This email is to confirm that you have accepted your talk proposals for ${ h.event_name() }. Thanks for making the conference what it is!
%elif c.status.name == 'Withdrawn':
This email is to confirm that you have withdrawn your talk proposals for ${ h.event_name() }. We’re sorry that you can’t come, but we understand that sometimes these things happen.
%elif c.status.name == 'Contact':
This email is to confirm that you have requested assistance with accepting your talk proposals for ${ h.event_name() }. A team member will be in contact as soon as possible to provide assistance.
%endif

Thanks and have a great day!

The ${ h.event_name() } team
