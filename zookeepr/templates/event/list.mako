<%inherit file="/base.mako" />

<h2>List Events</h2>

% if len(c.event_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Event Type</th>
    <th>Title</th>
    <th>Published</th>
    <th>Exclusive</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for event in c.event_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(event.id, h.url_for(action='view', id=event.id)) }</td>
    <td>${ h.link_to(event.type.name, h.url_for(controller='event_type', action='view', id=event.type.id)) }</td>
%     if event.proposal:
    <td>${ h.link_to(event.computed_title(), h.url_for(controller='proposal', action='view', id=event.proposal.id)) }</td>
%     else:
    <td>${ event.computed_title() }</td>
%     endif
    <td>${ h.yesno(event.publish) |n }</td>
    <td>${ h.yesno(event.exclusive) |n }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=event.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Event', url=h.url_for(action='new')) }</p>
    <p>${ h.link_to('Create Events from Proposals', url=h.url_for(action='new_proposals')) }</p>
% endif
 
