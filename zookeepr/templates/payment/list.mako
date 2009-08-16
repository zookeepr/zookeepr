<%inherit file="/base.mako" />

<h2>Payments</h2>
<table>

%if len(c.payment_collection) > 0:
  <tr>
    <th>id</th>
    <th>Invoice</th>
    <th>Amount</th>
    <th>Status</th>
    <th>First Name</th>
    <th>Last Name</th>
    <th>Email</th>
    <th>Created</th>
  </tr>
%endif

%for p in c.payment_collection:
  <tr class="${ h.cycle('odd', 'even') }">
    <td>${ h.link_to(p.id, url=h.url_for(action='view', id=p.id)) }</td>
    <td>${ p.invoice.id }</td>
    <td>${ h.number_to_currency(p.amount/100.0) }</td>
    <td>
% if len(p.payment_received) > 0:
%  if p.payment_received[0].approved:
Approved
%  else:
Declined
%  endif
% else:
-
% endif
    </td>
    <td>${ p.invoice.person.firstname }</td>
    <td>${ p.invoice.person.lastname }</td>
    <td><a href="mailto:${ p.invoice.person.email_address }">${ p.invoice.person.email_address }</a></td>
    <td>${ p.creation_timestamp |h }</td>
  </tr>
%endfor
</table>
