Subject: Confirmation of your registration to <% h.event_name() %>
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

Thankyou for registering for <% h.event_name() %>!

% if not c.signed_in_person:
Please validate your account by clicking on this URL:

http://<% h.host_name() %><% h.url_for('acct_confirm', confirm_hash=id) %>

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
 Dietary requirements:
    <% c.registration.diet %>

 Other requirements:
    <% c.registration.special %>

  Address: <% c.registration.person.address1 %>
           <% c.registration.person.address2 %>
           <% c.registration.person.city %>
           <% c.registration.person.state %>, <% c.registration.person.postcode %>
           <% c.registration.person.country %>
    Phone: <% c.registration.person.phone %>
  Company: <% c.registration.person.company %>
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
