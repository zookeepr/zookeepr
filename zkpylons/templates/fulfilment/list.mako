<%inherit file="/base.mako" />

<h2>List Fulfilment</h2>

% if len(c.fulfilment_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Person</th>
    <th>Type</th>
    <th>Status</th>
    <th>Code</th>
    <th>Completed</th>
    <th>Void</th>
    <th>Locked</th>
    <th>Can Edit</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for fulfilment in c.fulfilment_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(fulfilment.id, url=h.url_for(action='view', id=fulfilment.id)) }</td>
    <td>${ h.link_to(fulfilment.person.fullname, h.url_for(action='view', controller='person', id=fulfilment.person_id)) }</td>
    <td>${ fulfilment.type.name }</td>
    <td>${ fulfilment.status.name }</td>
    <td>${ fulfilment.code }</td>
    <td>${ h.yesno(fulfilment.is_completed) |n }</td>
    <td>${ h.yesno(fulfilment.is_void) |n }</td>
    <td>${ h.yesno(fulfilment.is_locked) |n }</td>
    <td>${ h.yesno(fulfilment.can_edit) |n }</td>
%     if fulfilment.type.name == 'Badge':
    <td>${ h.link_to('badge', url=h.url_for(action='badge_pdf', id=fulfilment.id)) }</td>
    <td>${ h.link_to('print', url=h.url_for(action='badge_print', id=fulfilment.id)) }</td>
%     else:
    <td></td>
    <td></td>
%     endif
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=fulfilment.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Fulfilment', url=h.url_for(action='new')) }</p>
% endif
 
