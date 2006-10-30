Subject: Confirmation of your registration to linux.conf.au 2007
To: <% c.person.fullname %> <<% c.person.email_address %>>

Dear <% c.person.fullname %>,

Thankyou for registering for linux.conf.au 2007!

If you would like to log into the linux.conf.au 2007 site, please
start by confirming your registration by clicking on the URL
below:

http://lca2007.linux.org.au<% h.url_for('acct_confirm', id=id) %>

(If clicking does not work, please clag it into your web browser.)

Once your account has been confirmed, you will be able to log
into the site with the password you provided with your registration.

Thanks again, and have a great day!

The linux.conf.au 2007 Organising Committee
<%args>
id
</%args>
<%doc>
This template is used to generate the email that is sent
to people registering for the conference.
</%doc>
