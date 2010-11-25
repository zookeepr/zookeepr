Subject: Regarding your volunteer application for ${ h.event_name() }
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>

Dear ${ c.person.firstname },

Thank you for your application to volunteer at ${ h.event_name() }.

%if c.volunteer.accepted:
You have been accepted as a volunteer for ${ h.event_name() }. Please:

1. Complete your registration by logging into the website and going to
${ h.url_for(quallifed=True, controller='registration' action='status', id=None) }. Please select
${ c.volunteer.ticket_type.description } when choosing your ticket.

2. Join our Volunteers Mailing list at
http://lists.followtheflow.org/mailman/listinfo/volunteers

Thank you for volunteering for ${ h.event_shortname() }!
%elif not c.volunteer.accepted:
You have not been selected as a volunteer for ${ h.event_name() } because we have
already filled all positions that suit your availability or skills.

Thank you again for your interest and we encourage you to volunteer
for next year!
%else:
Please add your self to the mailing list at http://lists.followtheflow.org/mailman/listinfo/volunteers.
%endif

Regards,
${ h.event_name() } Team
