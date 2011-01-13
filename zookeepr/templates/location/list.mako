<%inherit file="/base.mako" />

<h2>List Locations</h2>

% if len(c.location_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Display Name</th>
    <th>Display Order</th>
    <th>Capacity</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for location in c.location_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(location.id, url=h.url_for(action='view', id=location.id)) }</td>
    <td>${ location.display_name }</td>
    <td>${ location.display_order }</td>
    <td>${ location.capacity }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=location.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Location', url=h.url_for(action='new')) }</p>
% endif
 
