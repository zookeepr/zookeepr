<%inherit file="/base.mako" />

${ h.form(h.url_for(), method='get') }
<p class="entries" style="float: right">ID or name: ${ h.text('q', size=10, tabindex=1) }</p>
${ h.end_form() }

% if c.error:
%   if c.query:
Erroy looking up ${ c.query |h }:
%   endif

${ c.error }

% elif c.many:
<p>Looked up: ${ c.query } and found ${ len(c.many) }</p>
<table>
%   for person in c.many:
  <tr class="${ h.cycle("odd", "even") }">
    <td>${ h.link_to(person.fullname, h.url_for(p=person.id)) }</td>
    <td>
%     if person.registration:
%       if person.paid():
      <b>${ person.registration.ticket_description() }</b>
%       else:
      not paid
%       endif
%     else:
      no registration
%     endif
    </td>
  </tr>
%   endfor
</table>

% else:
<p>Looked up: ${ c.query }</p>

<p><b>${ c.person.firstname } ${ c.person.lastname }</b>
&lt;${ h.link_to(c.person.email_address) }&gt; (${ h.link_to(c.person.id, h.url_for(controller='person', action='view', id=c.person.id)) })
<br>${ c.person.company }</p>

<p>
%   if c.person.is_speaker():
<strong>speaker</strong><br>
%   endif
%   if c.person.roles:
<strong>${ ', '.join([role.name for role in c.person.roles]) }</strong><br>
%   endif

%   if c.person.registration:
<div style="float: right">
  ${ h.form(h.url_for(controller='rego_note', action='new', id=None), method='post') }
    ${ h.hidden('rego_note.rego', value=c.person.registration.id) }
    <table>
      <tr>
        <th>when</td>
        <th>note</td>
        <th>by</td>
      </tr>
%     for n in c.person.registration.notes:
      <tr class="${ h.cycle("odd", "even") }">
        <td>${ n.creation_timestamp.strftime('%Y-%m-%d %a %H:%M:%S') }</td>
        <td>${ n.note }</td>
        <td>${ n.by.firstname } ${ n.by.lastname }</td>
      </tr>
%     endfor
      <tr>
        <td>${ h.submit('submit', 'Add Note') }</td>
        <td>${ h.text('rego_note.note', size=30, tabindex=2, value='Here!') }</td>
        <td>${ h.text('rego_note.by', size=6, value=c.signed_in_person.id) }</td>
      </tr>
    </table>
  ${ h.end_form() }
</div>

%     if c.person.paid():
<b>${ c.person.registration.ticket_description() }</b> registration ${ h.link_to(c.person.registration.id, h.url_for(controller='registration', action='view', id=c.person.registration.id)) }
%     else:
<b>Tentative</b> registration ${ h.link_to(c.person.registration.id, h.url_for(controller='registration', action='view', id=c.person.registration.id)) }; <b>not paid</b>
%     endif
%   else:
not registered
%   endif
</p>

%   if c.person.phone:
<p>Phone: ${ c.person.phone }</p>
%   endif

<h2>Invoices</h2>
<p>${ h.link_to('New Manual Invoice', h.url_for(controller='invoice', action='new', id=None, person_id=c.person.id))}</p>
%   if c.person.invoices:
<table>
  <tr>
    <th>Invoice #</th>
    <th>Total</th>
    <th>Status</th>
  </tr>
%     for i in c.person.invoices:
  <tr class="${ h.cycle("odd", "even") }">
    <td>${ h.link_to(i.id, h.url_for(controller='invoice', action='view', id=i.id)) }</td>
    <td style="text-align: right">${ h.integer_to_currency(i.total) }</td>
    <td style="text-align: center">${ i.status }</td>
  </tr>
%     endfor
</table>
<br />
<table>
  <tr>
    <th>Invoice</td>
    <th>Description</td>
    <th>Qty</td>
    <th>Cost</td>
    <th>Total</td>
  </tr>
%   for i in c.person.invoices:
%     if not i.is_void:
%       for ii in i.items:
  <tr class="${ h.cycle("odd", "even") }">
%         if ii == i.items[0]:
    <td style="text-align: center" rowspan="${ len(i.items)}">
      ${ h.link_to(i.id, h.url_for(controller='invoice', action='view', id=i.id)) }<br />
      ${ i.status }
    </td>
%         endif
    <td>${ ii.description }</td>
    <td style="text-align: center">${ ii.qty }</td>
    <td style="text-align: right">${ h.integer_to_currency(ii.cost) }</td>
    <td style="text-align: right">${ h.integer_to_currency(ii.total) }</td>
  </tr>
%       endfor
%     endif
%   endfor
</table>
%   if c.person.fulfilments:
<h2>Fulfilments</h2>
<table>
  <tr>
    <th>Fulfilment</th>
    <th>Product</th>
    <th>Qty</th>
  </tr>
%     for f in c.person.fulfilments:
%       if not f.is_void:
%         for item in f.items:
  <tr class="${ h.cycle("odd", "even") }">
%           if item == f.items[0]:
    <td style="text-align: center" rowspan="${ len(f.items) }">
      ${ h.link_to(f.id, h.url_for(controller='fulfilment', action='view', id=f.id)) } - 
      ${ h.link_to('(edit)', h.url_for(controller='fulfilment', action='view', id=f.id)) }<br />
      ${ f.type.name } - ${ f.status.name }
    </td>
%           endif
    <td>${ item.product.category.name } - ${ item.product.description }</td>
    <td>${ item.qty }</td>
  </tr>
%         endfor
%       endif
%     endfor
</table>
%   endif

% endif

%   if c.person.registration:
<h2>Registration</h2>
<% c.registration = c.person.registration %>
<%include file="../registration/view_body.mako"/>
%   endif
% endif

