<%inherit file="/base.mako" />

    <h2>View Time Slot</h2>

    <p><b>id:</b> ${ c.time_slot.id }<br></p>
    <p><b>Start Time:</b> ${ c.time_slot.start_time.strftime('%d/%m/%y %H:%M:%S') }<br></p>
    <p><b>End Time:</b> ${ c.time_slot.end_time.strftime('%d/%m/%y %H:%M:%S') }<br></p>
    <p><b>Primary:</b> ${ h.yesno(c.time_slot.primary) | n }<br></p>

    <h3>This Time Slots schedule</h3>
    <table>
      <thead>
        <tr>
          <th>Location</th>
          <th>Event</th>
%if c.can_edit:
          <th></th>
          <th></th>
%endif
        </tr>
      </thead>
%for schedule in c.time_slot.schedule:
      <tbody>
        <tr>
          <td>${ h.link_to(schedule.location.display_name, url=h.url_for(controller='location', action='view', id=schedule.location.id)) }</td>
          <td>${ h.link_to(schedule.event.computed_title(), url=h.url_for(controller='event', action='view', id=schedule.event.id)) }</td>
%if c.can_edit:
          <td>${ h.link_to('Edit', url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }</td>
          <td>${ h.link_to('Delete', url=h.url_for(controller='schedule', action='delete', id=schedule.id)) }</td>
%endif
        </tr>
      </tbody>
%endfor
      <tfoot>
        <tr>
			<td colspan='4'>${ h.link_to('Add to schedule', url=h.url_for(controller='schedule', action='new', id=None, time_slot=c.time_slot.id)) }</td>
		</tr>
      </tfoot>
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>

