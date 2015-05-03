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

Accommodation
====================

Registering for the conference DOES NOT include your accommodation. It is your
own responsibility to make appropriate arrangements. Our venue, Wrest Point is 
offering discount rates for PyCon Australia delegates. For more information on 
how to book and alternative options please see 
http://2012.pycon-au.org/register/accommodation

We look forward to seeing you in Hobart!

The ${ c.config.get('event_name') } Organising Committee
