Subject: <% h.event_name() %> New Account Confirmation
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

If you would like to log into the linux.conf.au 2008 site, please
start by confirming your registration by clicking on the URL
below:

http://<% h.host_name() %><% h.url_for('acct_confirm', id=c.person.url_hash) %>

(If clicking does not work, please paste it into your web browser.)

Once your account has been confirmed, you will be able to log
into the site with the password you provided.

Don't forget to sign up to our announcements mailing list via
http://lists.mel8ourne.org/

Thanks, and have a great day!

The <% h.event_name() %> team
