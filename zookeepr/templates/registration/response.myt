Subject: Confirmation of your registration to <% h.event_name() %>
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

Thankyou for registering for <% h.event_name() %>!

% if not c.signed_in_person:
Please validate your account by clicking on this URL:

http://<% h.host_name() %><% h.url_for('acct_confirm', id=id) %>

(If clicking does not work, please paste it into your web browser.)

Once your account has been confirmed, you will be able to log into the web
site with the password you provided with your registration. You will then
be able to pay or view your invoice by visiting this page:
http://<% h.host_name() %>/registration/status
and follow the instructions to finalise your payment.

% else:

To pay or view your invoice, sign in to the website by visiting this page:
http://<% h.host_name() %>/registration/status
and follow the instructions to finalise your payment.

% #endif


Your registration details are:

   Ticket: <% c.registration.type %>

<%python>
teesize = c.registration.teesize.split('_')

try:
  teesize[0] = {
    'M': 'Mens',
    'F': 'Womens',
  }.get(teesize[0], teesize[0])

  teesize[1] = {
    'long': 'long-sleeve',
    'short': 'short-sleeve',
  }.get(teesize[1], teesize[1])
except:
  pass

teesize = ' '.join(teesize)

</%python>
 T-shirt: <% teesize %>

 Extra t-shirts: <% extra_tee_count |h %> (<% extra_tee_sizes |h %>)

 Extra tickets: <% c.registration.dinner |h %>

% if c.registration.accommodation:
%	a = c.registration.accommodation
%	if a.option:
%		opt = " (%s) " % a.option
%	else:
%		opt = ' '
%       def date_of(d):
%		if d==1:
%			return "%dst of February" % d
%		elif d==2:
%			return "%dnd of February" % d
%		elif d==3:
%			return "%drd of February" % d
%		elif d<15:
%			return "%dth of February" % d
%		elif d==31:
%			return "%dst of January" % d
%		else:
%			return "%dth of January" % d
%
%	accom = "%s%s(%s per night)" % (a.name, opt, h.number_to_currency(a.cost_per_night))
 Accommodation: <% accom %>
       Checkin: <% date_of(c.registration.checkin) %>
      Checkout: <% date_of(c.registration.checkout) %>
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
