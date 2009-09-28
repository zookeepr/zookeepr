Subject: Confirmation of your registration to ${ h.event_name() }
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>

Dear ${ c.person.firstname },

Thank you for registering for ${ h.event_name()}!

Your personal details are:

    Address: ${ c.registration.person.address1 }
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
      Phone: ${ c.registration.person.phone }
    Company: ${ c.registration.person.company }

If you wish to change your details, please log into the website.

%if c.student_ticket:
Please note, as part of the registration process, you may be required to present 
to the Registration Desk, either a student ID or proof of enrolment.

%endif
%if not c.person.paid():
Invoice
=======

You can view your invoice for payment:

    ${ h.lca_info['event_url'] + h.url_for(action='status') }

Please follow the instructions to finalise your payment. Payment must be
received before Friday 8 January 2010.

%endif
%if not c.person.is_speaker():
Accommodation
=============

LCA2010 have negotiated discounts with some local accommodation providers:

    http://www.lca2010.org.nz/register/accommodation

Please note, you *must* book your accommodation directly through the
accommodation providers. Registration on the LCA2010 website DOES NOT book
your accommodation. For any queries about the Accommodation, please contact
the Accommodation Providers directly.

%endif
%if c.person.country != 'NEW ZEALAND':
Immigration/Entry Requirements
==============================

Please note, New Zealand is a country in its own right. Anyone who lives
outside New Zealand (including Australia) will need a passport, and may
require a visa, to gain entry into New Zealand. Please contact your local
New Zealand Embassy department, well in advance of LCA2010, to determine
your travel needs. 

%endif
%if c.registration.diet:
Dietary Requirements
====================

In registering, you have noted a dietary requirement:

    ${c.registration.diet}

For health and safety reasons, please let us know how you react when you eat
the above foods, how severe the reaction is, and what medical attention you
need, if any, should a reaction occur.

%endif
%if c.registration.special:
Special Requirements
====================

In registering, you have noted the following special requirements:

    ${c.registration.special}

Please let us know you require any assistance at LCA2010 as a result of this.

%endif
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
Thank you for registering your Partner and children for the LCA2010 Partners
Programme.  Your partner will be contacted by our Partner Programme Coordinator 
on:
%else:
Thank you for registering your Partner for the LCA2010 Partners Programme.
Your partner will be contacted by our Partner Programme Coordinator on:
%endif

     partners@lca2010.org.nz

%endif
Open Day
========

The Open Day will be held on Saturday 23 January 2010. If you have an awesome
project, cool widgets or mind-blowing gadgets that will enthuse our attendees,
please contact us about getting a stall at the Open Day: openday@lca2010.org.nz

We look forward to seeing you in Wellington!

The ${ h.event_name() } Organising Committee
