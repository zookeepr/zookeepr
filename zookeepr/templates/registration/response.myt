Subject: Confirmation of your registration to <% h.event_name() %>
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

Thankyou for registering for <% h.event_name() %>!

% if not c.signed_in_person:
If you would like to log into the <% h.event_name() %> site, please
start by confirming your registration by clicking on the URL
below:

http://<% h.host_name() %><% h.url_for('acct_confirm', id=id) %>

(If clicking does not work, please paste it into your web browser.)

Once your account has been confirmed, you will be able to log
into the site with the password you provided with your registration.

% #endif

You can now view and pay for your invoice by visiting
http://<% h.host_name() %>/profile/<% c.person.id %> and
clicking on the "confirm and and pay" link. If you get a blank page
please ensure you are signed in.

Your account details are:

   Ticket: <% c.registration.type %>

<%python>
if c.registration.teesize.startswith('M'):
    teesex = 'Mens'
else:
    teesex = 'Womens'

teesize = {'S': 'small',
           'M': 'medium',
           'L': 'large',
           'XL': 'X large',
           'XXL': 'XX large',
           'XXXL': 'XXX large'}[c.registration.teesize[2:]]
</%python>
 Teeshirt: <% teesex %> <% teesize %>

 Extra tickets: <% c.registration.dinner |h %>

% if c.registration.accommodation:
%	a = c.registration.accommodation
%	if a.option:
%		opt = " (%s) " % a.option
%	else:
%		opt = ' '
%
%	accom = "%s%s(%s per night)" % (a.name, opt, h.number_to_currency(a.cost_per_night))
 Accommodation: <% accom %>
       Checkin: <% c.registration.checkin %>th January
      Checkout: <% c.registration.checkout %>th January
% else:
 Accommodation: none selected
% #endif

 Dietary requirements:
    <% c.registration.diet %>

 Other requirements:
    <% c.registration.special %>

  Address: <% c.registration.address1 %>
           <% c.registration.address2 %>
           <% c.registration.city %>
           <% c.registration.state %>, <% c.registration.postcode %>
           <% c.registration.country %>
    Phone: <% c.registration.phone %>
  Company: <% c.registration.company %>
 IRC Nick: <% c.registration.nick %>

    Shell: <% c.registration.shelltext or c.registration.shell %>
   Editor: <% c.registration.editortext or c.registration.editor %>
   Distro: <% c.registration.distrotext or c.registration.distro %>

If you want to change your details, please log into the website.

Thanks again, and have a great day!

The <% h.event_name() %> Organising Committee
<%args>
id
</%args>
<%doc>
This template is used to generate the email that is sent
to people registering for the conference.
</%doc>
