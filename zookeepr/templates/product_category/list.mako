<%inherit file="/base.mako" />

<h2>List of categories</h2>

% if len(c.product_category_collection) > 0:
<table>
  <tr>
    <th>Name</th>
    <th>Description</th>
    <th>Display</th>
    <th>Display Order</th>
    <th>Min. Quantity</th>
    <th>Max. Quantity</th>
    <th>&nbsp;</th>
  </tr>
%   for category in c.product_category_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(category.name, url=h.url_for(action='view', id=category.id)) }</td>
    <td>${ category.description |n}</td>
    <td>${ category.display }</td>
    <td>${ category.display_order }</td>
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
 
