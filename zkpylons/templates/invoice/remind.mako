<%inherit file="/base.mako" />

${ h.form(h.url_for()) }

<p>The message below will be sent to the owners of all checked invoices below</p>

<pre>
<%include file="remind_email.mako" />
</pre>

<table>
  <tr>
    <th>Remind</th>
    <th>Name</th>
    <th>Invoice</th>
    <th>Email Address</th>
    <th>Status</th>
  </tr>
% for i in c.invoice_collection:
%   if i. or i.person.paid():
<%    continue %>
%   endif
  <tr>
    <td>${ h.checkbox('invoices', value=i.id, checked=True) }</td>
    <td>${ h.link_to(i.person.firstname + ' ' + i.person.lastname, url=h.url_for(controller='person', action='view', id=i.person.id)) }</td>
    <td>${ h.link_to(h.integer_to_currency(i.total), url=h.url_for(action='view', id=i.id)) }
    <td>${ i.person.email_address }</td>
    <td>
%   if not i.payments:
      Not Paid
%   elif len(i.bad_payments) > 0:
      Incomplete Payments
%   else:
      Unknown
%   endif
    </td>
% endfor
  </tr>
</table>
${ h.submit('submit', 'Send Reminder') }

