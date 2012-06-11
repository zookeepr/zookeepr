<%inherit file="/base.mako" />

<h2>List Scheduled Events</h2>

% if len(c.schedule_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Time Slot</th>
    <th>Location</th>
    <th>Event</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for schedule in c.schedule_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(schedule.id, h.url_for(action='view', id=schedule.id)) }</td>
    <td>${ h.link_to(schedule.time_slot.description, url=h.url_for(controller='time_slot', action='view', id=schedule.time_slot_id)) }</td>
    <td>${ h.link_to(schedule.location.display_name, url=h.url_for(controller='location', action='view', id=schedule.location_id)) }</td>
    <td>${ h.link_to(schedule.event.computed_title(), url=h.url_for(controller='event', action='view', id=schedule.event_id)) }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=schedule.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Schedule', url=h.url_for(action='new')) }</p>
% endif
 
