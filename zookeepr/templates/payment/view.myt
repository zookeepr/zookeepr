<h1>Payment</h1>

<p>
% if c.payment.result != 'OK':
This is an invalid payment. Please contact seven-contact@lca2007.linux.org.au
% elif c.payment.Status == 'Accepted':
Your payment was successful. Your receipt number is <% c.payment.id %>
% else:
Your payment was unsuccessful. The reason was:
</p>
<p>
<b>
<% c.payment.ErrorString %>
</b>
</p>
<p>
Try to
<% h.link_to('(confirm invoice and pay)', url=h.url(controller='registration', action='pay', id=c.profile.registration.id)) %>
again.

% #endiff
</p>
<p>
Back to 
<% h.link_to('my profile', url=h.url(controller='profile', action='index')) %>
.
</p>
