<%inherit file="/base.mako" />

    <h2>View Location</h2>

    <p><b>Display Name:</b> ${ c.location.display_name }<br></p>
    <p><b>Display Order:</b> ${ c.location.display_order }<br></p>
    <p><b>Capacity:</b> ${ c.location.capacity }<br></p>

    <h3>This locations schedule</h3>
    <table>
      <thead>
        <tr>
          <th>Time Slot</th>
          <th>Event</th>
%if c.can_edit:
          <th></th>
          <th></th>
%endif
        </tr>
      </thead>
%for schedule in c.location.schedule:
      <tbody>
        <tr>
          <td>${ h.link_to(schedule.time_slot.description, url=h.url_for(controller='time_slot', action='view', id=schedule.time_slot.id)) }</td>
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
          <td colspan='4'>${ h.link_to('Add to schedule', url=h.url_for(controller='schedule', action='new', location=c.location.id)) }</td>
      </tfoot>
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
