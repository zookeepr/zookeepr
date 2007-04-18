Subject: Confirmation of your payment attempt for linux.conf.au 2007
To: <% c.person.firstname %>  <% c.person.lastname %> <<% c.person.email_address %>>

Thank you for your payment attempt, the results are below.

<p>
% if c.payment.result != 'OK':
This is an invalid payment. Please contact seven-contact@lca2007.linux.org.au
% elif c.payment.Status == 'Accepted':
Your payment was successful. Your receipt number is <% c.payment.id %>
You can view your invoice at http://lca2007.linux.org.au/invoice/<% c.payment.invoice.id %>
% else:
Your payment was unsuccessful. The reason was:

    <% c.payment.ErrorString %>

You can try again by visiting http://lca2007.linux.org.au/registration/<% c.payment.invoice.person.registration.id %>/pay

% #endiff

Thanks again, and have a great day!

The linux.conf.au 2007 Organising Committee
<%args>
id
</%args>
<%doc>
This template is used to generate the email that is sent
to people registering for the conference.
</%doc>

