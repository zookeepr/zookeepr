<%inherit file="/base.mako" />

<h2>Ceiling Special Cases - ${ c.ceiling.name }</h2>

<p>${ h.link_to('Back to ' + c.ceiling.name, url=h.url_for(action='view')) }</p>

<a name="diet_special_paid"></a>
<h3>Diet/Special - Paid</h3>
${ list() }

<a name="diet_special_invoiced"></a>
<h3>Diet/Special - Invoiced (Not Paid)</h3>
${ list(paid = False) }

<a name="diet_paid"></a>
<h3>Diet - Paid</h3>
${ diet() }

<a name="diet_paid"></a>
<h3>Diet - Invoiced (Not Paid)</h3>
${ diet(paid = False) }

<a name="under18_paid"></a>
<h3>Under 18 - Paid</h3>
${ under18() }

<a name="under18_invoiced"></a>
<h3>Under 18 - Invoiced (Not Paid)</h3>
${ under18(paid = False) }

<%def name="list(paid=True)">
<table>
  <thead><tr>
    <th>Person</th>
    <th>Rego ID</th>
    <th>Product</th>
    <th>Diet</th>
    <th>Special Needs</th>
  </tr></thead>
  <tbody>
% for product in c.ceiling.products:
%   for invoice_item in product.invoice_items:
%     if not invoice_item.invoice.status == 'Invalid' and ((paid and invoice_item.invoice.is_paid) or not (paid or invoice_item.invoice.is_paid)):
<%       rego = invoice_item.invoice.person.registration %>
%       if rego.diet is not '' or rego.special is not '':
  <tr>
    <td>${ h.link_to(invoice_item.invoice.person.fullname(), h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
    <td>${ h.link_to('rego id: ' + str(rego.id), url=h.url_for(controller='registration', action='view', id=rego.id)) }</td>
    <td>${ invoice_item.description }</td>
    <td>${ rego.diet }</td>
    <td>${ rego.special }</td>
  </tr>
%         for note in rego.notes:
  <tr>
    <td>&nbsp;</td>
    <td colspan="4">${ note.note }</td>
  </tr>
%         endfor
%       endif
%     endif
%   endfor
% endfor
  <tbody>
</table>
</%def>

<%def name="diet(paid=True)">
<table>
  <thead><tr>
    <th>Diet</th>
    <th>People</th>
  </tr></thead>
  <tbody>
<%
  diet = {}
  for product in c.ceiling.products:
    for invoice_item in product.invoice_items:
      if not invoice_item.invoice.status == 'Invalid' and ((paid and invoice_item.invoice.is_paid) or not (paid or invoice_item.invoice.is_paid)):
        rego = invoice_item.invoice.person.registration 
        if rego.diet is not '':
          if rego.diet not in diet:
            diet[rego.diet] = {}
          if rego.person.lastname not in diet[rego.diet]:
            diet[rego.diet][rego.person.lastname] = []
          diet[rego.diet][rego.person.lastname].append(rego)
  diets = diet.keys()
  diets.sort()
%>

% for d in diets:
<%
    surnames = diet[d].keys()
    surnames.sort()
    names = []
    for surname in surnames:
      for rego in diet[d][surname]:
        names.append(h.link_to(rego.person.fullname(), h.url_for(controller='person', action='view', id=rego.person.id)))
%>
  <tr>
    <td>${ d }</td>
    <td>${ ", ".join(names) | n }</td>
  </tr>
%     endfor
  <tbody>
</table>
</%def>

<%def name="under18(paid=True)">
<table>
  <thead><tr>
    <th>Person</th>
    <th>Rego ID</th>
    <th>Product</th>
  </tr></thead>
  <tbody>
% for product in c.ceiling.products:
%   for invoice_item in product.invoice_items:
%     if not invoice_item.invoice.status == 'Invalid' and ((paid and invoice_item.invoice.is_paid) or not (paid or invoice_item.invoice.is_paid)):
<%       rego = invoice_item.invoice.person.registration %>
%       if not rego.over18:
  <tr>
    <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
    <td>${ h.link_to('rego id: ' + str(rego.id), url=h.url_for(controller='registration', action='view', id=rego.id)) }</td>
    <td>${ invoice_item.description }</td>
  </tr>
%       endif
%     endif
%   endfor
% endfor
  <tbody>
</table>
</%def>


<%def name="contents()">
<%
  menu =  '<li><a href="#diet_special_paid">Diet/Special - Paid</a></li>'
  menu += '<li><a href="#diet_special_invoiced">Diet/Special - Invoiced</a></li>'
  menu += '<li><a href="#diet_paid">Diet - Paid</a></li>'
  menu += '<li><a href="#diet_invoiced">Diet - Invoiced</a></li>'
  menu += '<li><a href="#under18_paid">Under 18 - Paid</a></li>'
  menu += '<li><a href="#under18_invoiced">Under 18 - Invoiced</a></li>'

  return menu
%>
</%def>
<%def name="title()">
Special Cases - ${ c.ceiling.name } - ${ parent.title() }
</%def>

