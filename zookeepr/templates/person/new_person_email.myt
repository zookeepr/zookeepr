Subject: <% h.event_name() %> New Account Confirmation
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

Thank you for creating a login to the <% h.event_name() %> website.
Please validate your account by clicking on this URL:

http://<% h.host_name() %><% h.url_for('acct_confirm', confirm_hash=c.person.url_hash) %>

(If clicking does not work, please paste it into your web browser.)

Once your account has been confirmed, you will be able to log into the web
site with the password you provided.

Thanks, and have a great day!

The <% h.event_name() %> team
http://<% h.host_name() %>/contact
