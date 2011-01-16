Subject: Regarding your volunteer application for ${ h.event_name() }
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>

Dear ${ c.person.firstname },

Thank you for your application to volunteer at ${ h.event_name() }.

%if c.volunteer.accepted == True:
You have been accepted as a volunteer for ${ h.event_name() }. Please:

1. Complete your registration by logging into the website and going to
${ h.url_for(qualified=True, controller='registration', action='status', id=None) }. 
%  if c.volunteer.ticket_type:
Please select ${ c.volunteer.ticket_type.description } when choosing your ticket.
%  endif

2. Join our Volunteers Mailing list at
http://lists.followtheflow.org/mailman/listinfo/volunteers

Thank you for volunteering for ${ h.event_shortname() }!
%elif c.volunteer.accepted == False:
You have not been selected as a volunteer for ${ h.event_name() } because we have
already filled all positions that suit your availability or skills.

Thank you again for your interest and we encourage you to volunteer for next year!
%else:
We will be in contact shortly regarding your application.
%endif

Regards,
${ h.event_name() } Team
