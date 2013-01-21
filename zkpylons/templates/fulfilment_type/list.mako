<%inherit file="/base.mako" />

<h2>List Fulfilment Types</h2>

% if len(c.fulfilment_type_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Display Name</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for fulfilment_type in c.fulfilment_type_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(fulfilment_type.id, url=h.url_for(action='view', id=fulfilment_type.id)) }</td>
    <td>${ fulfilment_type.name }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=fulfilment_type.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Fulfilment Type', url=h.url_for(action='new')) }</p>
% endif
 
