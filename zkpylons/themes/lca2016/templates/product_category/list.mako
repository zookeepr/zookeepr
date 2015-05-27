<%inherit file="/base.mako" />

<h2>List of categories</h2>

% if len(c.product_category_collection) > 0:
<table class="table sortable">
  <tr>
    <th>Name</th>
    <th>Description</th>
    <th>Note</th>
    <th>Display</th>
    <th>Display Mode</th>
    <th>Display Order</th>
    <th>Invoice Free Products</th>
    <th>Min. Quantity</th>
    <th>Max. Quantity</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for category in c.product_category_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(category.name, url=h.url_for(action='view', id=category.id)) } <br /><sub>(${h.link_to('Statistics', url=h.url_for(action='stats', id=category.id))})</sub></td>
    <td>${ category.description |n}</td>
    <td>${ category.note or "" |n}</td>
    <td>${ category.display }</td>
    <td>${ category.display_mode or ""}</td>
    <td>${ category.display_order }</td>
    <td>${ h.yesno(category.invoice_free_products) |n}</td>
    <td>${ category.min_qty }</td>
    <td>${ category.max_qty }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=category.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Product Category', url=h.url_for(action='new')) }</p>
% endif
 
