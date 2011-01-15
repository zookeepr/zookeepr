<%inherit file="/base.mako" />

<h2>List Time Slots</h2>

% if len(c.time_slot_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Start Date/Time</th>
    <th>End Date/Time</th>
    <th>Primary</th>
    <th>Heading</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for time_slot in c.time_slot_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(time_slot.id, url=h.url_for(action='view', id=time_slot.id)) }</td>
    <td>${ time_slot.start_time.strftime('%d/%m/%y %H:%M:%S') }</td>
    <td>${ time_slot.end_time.strftime('%d/%m/%y %H:%M:%S') }</td>
    <td>${ h.yesno(time_slot.primary) |n}</td>
    <td>${ h.yesno(time_slot.heading) |n}</td>
%     if c.can_edit:
%       for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=time_slot.id)) }</td>
%       endfor
%     endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Time Slot', url=h.url_for(action='new')) }</p>
% endif
 
