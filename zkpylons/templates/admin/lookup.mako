<%inherit file="/base.mako" />

<%

def if_then_else(cond, yes, no):
  if cond:
    return yes
  else:
    return no

def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven1 = oddeven().next
oddeven2 = oddeven().next

registration = c.r
person = c.p
invoices = c.i

%>

${ h.form(h.url_for(), method='get') }
<p class="entries" style="float: right">ID or name: ${ h.text('id', size=10, tabindex=1) }</p>
${ h.end_form() }
% if c.error:
%   if c.id:
Error looking up ${ c.id |h }:
%   endif
${ c.error }
% elif c.many:
<p>Looked up: ${ c.id } and found ${ len(c.many) }</p>
<table>
%   for p, typ in c.many:
  <tr class="${ oddeven1() }">
    <td><a href="/admin/lookup?p_id=${ p.id }" tabindex="2">${ p.firstname }
					       ${ p.lastname }</td>
    <td>(${ typ })
    <td>
%     if p.registration:
%       if p.invoices and p.invoices[0].paid():
	  <b>${ p.registration.ticket_description() }</b>
%       else:
	  not paid
%       endif
%     else:
	no rego
%     endif
  </tr>
%   endfor
</table>
% else:
<p>Looked up: ${ c.id } (${ c.id_type })</p>

<p><b>${ person.firstname } ${ person.lastname }</b>
&lt;<a href="mailto:${ person.email_address }">${ person.email_address }</a>&gt; (<a href="/person/${ person.id }">${ person.id }</a>)
<br>${ person.company }</p>

<p>
%   if person.is_speaker():
<strong>speaker</strong><br>
%   endif
%   if person.roles:
<strong>${ ', '.join([role.name for role in person.roles]) }</strong><br>
%   endif
%   if registration:
${ h.form(h.url_for(), method='post') }
<p class="entries" style="float: right">Add note:
${ h.text('note', size=30, tabindex=2, value='Here!') }
${ h.hidden('id', value=registration.id) }
</p>
${ h.end_form() }
%     if invoices and invoices[0].paid():
<b>${ registration.ticket_description() }</b> rego <a href="/registration/${registration.id}">${registration.id}</a>
%     else:
<b>Tentative</b> rego <a href="/registration/${registration.id}">${registration.id}</a>; <b>not paid</b>
%     endif
%   else:
not registered
%   endif
</p>

%   if person.phone:
<p>Phone: ${ person.phone }</p>
%   endif

<p>
%   if invoices:
%     for i in invoices:
invoice <a href="/invoice/${i.id}">${ i.id }</a> (${ h.number_to_currency(i.total/100.0) } ${ if_then_else(i.paid(), 'paid', 'not paid')})
%     endfor
%   endif
</p>

% if invoices:
<table width="100%">
  <tr>
    <th>Invoice</td>
    <th>Description</td>
    <th>Qty</td>
    <th>Cost</td>
    <th>Total</td>
  </tr>
%   for i in invoices:
%     for ii in i.items:
  <tr class="${ oddeven1() }">
    <td align="center">${ i.id }${ if_then_else(i.paid(), '', ' (unpaid)')}</td>
    <td>${ ii.description }</td>
    <td align="center">${ ii.qty }</td>
    <td align="right">${ h.number_to_currency(ii.cost/100.0) }</td>
    <td align="right">${ h.number_to_currency(ii.total/100.0) }</td>
  </tr>
%     endfor
%   endfor
</table>
% endif

% if registration and registration.notes:
<table width="100%">
  <tr>
    <th>when</td>
    <th>note</td>
    <th>by</td>
  </tr>
%   for n in registration.notes:
  <tr class="${ oddeven2() }">
    <td align="left">${ n.entered.strftime('%Y-%m-%d %a %H:%M:%S') }</td>
    <td align="left">${ n.note }</td>
    <td align="left">${ n.by.firstname } ${ n.by.lastname }</td>
  </tr>
%   endfor
</table>
% endif

<h2>Registration</h2>
%   if registration:
<% c.registration = registration %>
<%include file="../registration/view_body.mako"/>
%   endif
% endif

