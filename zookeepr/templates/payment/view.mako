<%inherit file="/base.mako" />

<h1>Payment</h1>

<p>
% if c.payment.result != 'OK':
This is an invalid payment. Please contact ${ h.contact_email() }
% elif c.payment.Status == 'Accepted':
Your payment was successful. Your receipt number is ${ c.payment.id }
% else:
Your payment was unsuccessful. The reason was:
</p>
<p>
<b>
${ c.payment.ErrorString }
</b>
</p>
<p>
Try to
${ h.link_to('(confirm invoice and pay)', url=h.url_for(controller='registration', action='pay', id=c.payment.invoice.person.registration.id)) }
again.

% endif
</p>
<p>
Back to 
${ h.link_to('my profile', url=h.url_for(controller='profile', action='index')) }
.
</p>
