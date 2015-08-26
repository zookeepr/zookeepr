From: <% c.config.get('event_name') %> <<% c.config.get('contact_email') %>>
To: <% c.fullname %> <<% c.email %>>
Subject: Please review your <% c.config.get('event_name') %> registration details

Dear <% c.firstname %>,

This is a reminder of your <% c.config.get('event_name') %> registration.

% if c.speaker:
*** Remember that if you want your partner to come to the speakers'
dinner, his or her details need to be included in your account. ***

% #endif
  Name:     <% c.fullname %>
% if len(c.company) > 0:
  Company:  <% c.company %>
% #endif
  Email:    <% c.email %>
  Phone:    <% c.phone %>
  Mobile:   <% c.mobile %> 
  Address:  <% c.address %>

Please make sure that your details are correct. If you need to change
anything, log into your account at:

  <% c.config.get('event_url') %>

If you have any problems, feel free to email <% c.config.get('contact_email') %>.

Regards,

The <% c.config.get('event_name') %> team

<%doc>
This template is used to generate the email that is sent to every
attendee who has paid.

That manual email function is located on the admin page.
</%doc>
