Subject: Confirmation of your registration to linux.conf.au 2007
To: <% c.person.fullname %> <<% c.person.email_address %>>

Dear <% c.person.fullname %>,

Thankyou for registering for linux.conf.au 2007!

% if not c.signed_in_person:
If you would like to log into the linux.conf.au 2007 site, please
start by confirming your registration by clicking on the URL
below:

http://lca2007.linux.org.au<% h.url_for('acct_confirm', id=id) %>

(If clicking does not work, please clag it into your web browser.)

Once your account has been confirmed, you will be able to log
into the site with the password you provided with your registration.

% #endif
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

    Shell: <% c.registration.shelltext or c.registration.shell %>
   Editor: <% c.registration.editortext or c.registration.editor %>
   Distro: <% c.registration.distrotext or c.registration.distro %>

If you want to change your details, please log into the website.

Please note!  You have not yet been invoiced.  Your invoice will be sent
to you via email when ready.

Thanks again, and have a great day!

The linux.conf.au 2007 Organising Committee
<%args>
id
</%args>
<%doc>
This template is used to generate the email that is sent
to people registering for the conference.
</%doc>
