<%inherit file="/base.mako" />

<h1>Payment</h1>

%if c.payment is None:
% if c.is_organiser:
<p>This payment object doesn't have a matching payment_received object.</p>
% else:
<p>We haven't received anything back from the payment gateway.</p>

<p>Please ${ h.link_to('try again', url=h.url_for(controller='registration', action='pay', id=c.person.registration.id)) }. If you still run into problems, email us at ${ h.contact_email() }</p>
% endif

%elif c.is_organiser:

<p>
<table>
<tr><td valign="top"><b>Status:</b></td>
<td>
% if c.payment.approved:
<font color="green">Approved</font>
% else:
<font color="red">Not approved</font>
% endif
<br>(${ c.payment.success_code } - ${ c.payment.response_text })
</td>
</tr>

%  if c.validation_errors:
<tr><td valign="top"><b><font color="red">Zookeepr validation errors:</font></b></td>
<td>${ '<br>'.join(c.validation_errors) | n}</td></tr>
%  endif

<tr><td valign="top"><b>Invoice:</b></td>
%if c.payment.invoice is None:
<td><font color="red">None found</font></td>
%else:
<td>${ h.link_to(c.payment.invoice.id, url=h.url_for(controller='invoice', action='view', id=c.payment.invoice.id)) }
(${ c.payment.invoice.status })
%  if c.payment.payment not in c.payment.invoice.payments:
<font color="red">(INVALID)</font>
%  endif
</td></tr>
%endif

<tr><td valign="top"><b>Amount paid:</b></td>
<td>${ h.number_to_currency(c.payment.amount_paid / 100.0) } (charged in ${ c.payment.currency_used })</td></tr>

<tr><td valign="top"><b>Payment gateway:</b></td>
<td>Auth: ${ c.payment.auth_code }
<br>Reference: ${ c.payment.gateway_ref }</td></tr>

%  if c.payment.card_type is not None:
<tr><td valign="top"><b>${ c.payment.card_type } Card:</b></td>
<td>${ c.payment.card_name }
<br>${ c.payment.card_number }
<br>${ c.payment.card_expiry }
</td></tr>
<!--
<tr><td><b>Card MAC:</b></td>
<td>${ c.payment.card_mac }</td></tr>
-->
%  endif

<tr><td valign="top"><b>Email address:</b></td>
<td>${ c.payment.email_address }</td></tr>

<tr><td valign="top"><b>Client IP:</b></td>
<td>${ c.payment.client_ip_zookeepr } (zkpylons)<br>
${ c.payment.client_ip_gateway } (gateway)</td></tr>

<tr><td valign="top"><b>Timestamp:</b></td>
<td>${ c.payment.creation_timestamp } (created)
<br>${ c.payment.last_modification_timestamp } (modified)</td></tr>

</table>
</p>

%else:

% if c.payment.approved:
<p>Your payment was <b>successful</b>.</p>
<p>Your receipt number is: <b>PR${ c.payment.id }P${ c.payment.payment.id }</b></p>
% else:
<p>Your payment was <b>unsuccessful</b>.</p>
<p>The reason was:
<blockquote>${ c.payment.response_text }</blockquote>
</p>

<p>Please ${ h.link_to('try again', url=h.url_for(controller='registration', action='pay', id=c.person.registration.id)) }. If you still run into problems, email us at ${ h.contact_email() }</p>
% endif

%endif

%if c.is_organiser:

%  if len(c.related_payments) > 0:
<p>Related payments:
<ul>
%    for pr in c.related_payments:
<li>${ h.link_to(str(pr.payment.id), url=h.url_for(controller='payment', action='view', id=pr.payment.id)) }
(${ pr.creation_timestamp })</li>
%    endfor
</ul>
</p>
%  endif

<p>Back to ${ h.link_to('payment list', url=h.url_for(controller='payment', action='index')) }.</p>
%else:
<p>Back to ${ h.link_to('registration page', url=h.url_for(controller='registration', action='status',  id=c.person.registration.id)) }.</p>
%endif
