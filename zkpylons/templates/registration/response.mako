Subject: Confirmation of your registration to ${ c.config.get('event_name') }
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>

Dear ${ c.person.firstname },

Thank you for registering for ${ c.config.get('event_name')}!

Your personal details are:

    Address:
             ${ c.registration.person.address1 }
%if c.registration.person.address2:
             ${ c.registration.person.address2 }
%endif
%if c.registration.person.state:
             ${ c.registration.person.city }
             ${ c.registration.person.state }, ${ c.registration.person.postcode }
%else:
             ${ c.registration.person.city }, ${ c.registration.person.postcode }
%endif
             ${ c.registration.person.country }
      Phone:
             ${ c.registration.person.phone }
    Company:
             ${ c.registration.person.company }

If you wish to change your details, please log into the website.

%if c.student_ticket:
Please note, as part of the registration process, you will be required to present 
to the Registration Desk, either a student ID or proof of enrolment.

%endif
%if not c.person.paid():
Invoice
=======

You can view your invoice for payment:

    ${ h.url_for(qualified=True, controller='registration', action='status') }

Registering for the conference DOES NOT HOLD YOUR TICKET until it has
been paid in full. So to ensure that you secure your ticket, pay the
registration invoice as soon as possible.

%endif

%if c.registration.diet:
Dietary Requirements
====================

In registering, you have noted a dietary requirement:

    ${c.registration.diet}

Thank you for providing this information, we will be in contact with you if we
need any further clarification.

%endif
%if c.registration.special:
Special Requirements
====================

In registering, you have noted the following special requirements:

    ${c.registration.special}

Thank you for providing this information, we will be in contact with you if we
need any further clarification.

%endif
<%doc>
%if c.infants:
Infants
=======

In registering, you have noted you will be bringing infants to the social
events. Please note the social event venues have the following facilities:

    * Change table
    * High chair
    * Bottle warming facilities
    * Buggy accessibility

Please note infants (aged 0-1) will not be provided a seat or meal. If your baby
needs solid food, please bring it along with you. If you require a high chair,
please let us know so that we can reserve one for your baby to use.

%endif
</%doc>
%if c.children:
Children
========

Please note, if you have selected child, your child will receive a child's
meal. If your child needs an adult meal, then please edit your registration
form and select another 'adult' ticket instead of a 'child' ticket.

%endif
%if c.registration.partner_name:
Partners Programme
==================

%if c.pp_children:
Thank you for registering your Partner and children for the ${ c.config.get('event_shortname') } Partners
Programme.  Your partner will be contacted by our Partner Programme Coordinator 
on:
%else:
Thank you for registering your Partner for the ${ c.config.get('event_shortname') } Partners Programme.
Your partner will be contacted by our Partner Programme Coordinator on:
%endif

     partners@lcaunderthestars.org.au

%endif


We look forward to seeing you in ${ c.config.get('event_city') }!

The ${ c.config.get('event_name') } Organising Committee
