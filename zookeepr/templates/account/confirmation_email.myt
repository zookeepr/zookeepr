From: <% h.event_name() %> <%h.contact_email() %>
Subject: <% h.event_name() %> Forgotten Password Reset Confirmation
To: <% c.conf_rec.email_address %>

To initiate the process for resetting the control panel password for
<% c.conf_rec.email_address %>, please click on the link below:

http://<% h.host_name() %><% h.url_for(controller='account', action='reset_password', url_hash=c.conf_rec.url_hash) %>

If clicking the link does not work, copy and paste it into your web
browser.

Please note that this URL will expire after 24 hours.

If there are any problems, please contact us by replying to this
message.

If you didn't ask for your password to be reset, you can ignore this
message as your password has not been changed yet.  The request will
expire in 24 hours.
