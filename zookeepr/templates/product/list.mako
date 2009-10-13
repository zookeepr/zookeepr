<%inherit file="/base.mako" />
<%
  import re 
  grand_total = 0
  count = 0
%>

    <h2>List products</h2>
    <p><b>Note:</b> Totals are not necessarily accurate as they do not take into account for vouchers. They are simply paid items times cost.</p>
% if len(c.product_categories) > 0:
%   for category in c.product_categories:
<%
      simple_title = re.compile('([^a-zA-Z0-9])').sub('', category.name) 
      count = count + 1
%>

    <table>
      <tr>
        <a name="${ simple_title }"></a>
        <td colspan="10" align="center"><h3>${ category.name }</h3></td>
      </tr>
      <thead><tr>
        <th>Description</th>
        <th>Active</th>
        <th>Available</th>
        <th>Cost</th>
        <th>Invoiced (inc. overdue)</th>
        <th>Valid Invoices</th>
        <th>Sold</th>
        <th>Free</th>
        <th>Total</th>
        <th>&nbsp;</th>
        <th>&nbsp;</th>
      </tr></thead>
%       if len(category.products) > 0:
<%           cat_total = 0 %>
%           for product in category.products:
<%               cat_total += (product.qty_sold() * product.cost) %>
      <tr class="${ h.cycle('odd', 'even') }">
        <td>${ h.link_to(product.description, url=h.url_for(action='view', id=product.id)) }</td>
        <td>${ h.yesno(product.active) |n }</td>
        <td>${ h.yesno(product.available()) |n }</td>
        <td>${ h.number_to_currency(product.cost/100.0) | h }</td>
        <td>${ product.qty_invoiced(date = False) }</td>
        <td>${ product.qty_invoiced() }</td>
        <td>${ product.qty_sold() }</td>
        <td>${ product.qty_free() }</td>
        <td>${ h.number_to_currency((product.qty_sold() * product.cost)/100) }</td>
%               if c.can_edit:
%                   for action in ['edit', 'delete']:
        <td>${ h.link_to(action, url=h.url_for(action=action, id=product.id)) }</td>
%                   endfor
%               endif
      </tr>
%           endfor
<%           grand_total += cat_total %>
        <tr>
            <td colspan="8" style="font-weight: bold; text-align: right;">Sub-Total:</td>
            <td colspan="3">${ h.number_to_currency(cat_total/100) }</td>
        </tr>
%       endif
%       if count == len(c.product_categories):
        <tr>
            <td colspan="8" style="font-weight: bold; text-align: right;">Grand Total:</td>
            <td colspan="3">${ h.number_to_currency(grand_total/100) }</td>
        </tr>
%       endif
    </table>
%   endfor
% endif

<p>${ h.link_to('New product', url=h.url_for(action='new')) }</p>

<%def name="contents()">
<%
  menu = ''

  import re

  for category in c.product_categories:
    simple_title = re.compile('([^a-zA-Z0-9])').sub('', category.name) 
    menu += '<li><a href="#' + simple_title + '">' + category.name + ' products</a></li>' 
  return menu
%>
</%def>
<%def name="title()">
Products -
 ${ parent.title() }
</%def>

