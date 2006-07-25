Subject: Confirmation of your submission to the LCA 2007 CFP
To: <% c.registration.email_address %>

Thankyou for your submission entitled "<% c.submission.title %>".

If you would like to log into the LCA 2007 site, please
start by confirming your registration by clicking on the URL
below:

http://lca2007.linux.org.au<% h.url_for(controller='register', action='confirm', id=id) %>

(If clicking does not work, please clag it into your web browser.)

Once your account has been confirmed, you will be able to log
into the site with the password you provided with your submission.

Thanks again, and have a great day!

<%args>
id
</%args>
<%doc>
This template is used to generate the email that is sent
to people submitting to the CFP
</%doc>
