<%inherit file="/base.mako" />

<h2>List Fulfilment Status</h2>

% if len(c.fulfilment_status_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Name</th>
    <th>Vod</th>
    <th>Completed</th>
    <th>Locked</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for fulfilment_status in c.fulfilment_status_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(fulfilment_status.id, url=h.url_for(action='view', id=fulfilment_status.id)) }</td>
    <td>${ fulfilment_status.name }</td>
    <td>${ h.yesno(fulfilment_status.void) |n }</td>
    <td>${ h.yesno(fulfilment_status.completed) |n }</td>
    <td>${ h.yesno(fulfilment_status.locked) |n }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=fulfilment_status.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Fulfilment Status', url=h.url_for(action='new')) }</p>
% endif
 
