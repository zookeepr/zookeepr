<%inherit file="/base.mako" />

    <h2>View Event</h2>

    <p><b>Event Type:</b> ${ c.event.type.name }<br></p>
%if c.proposal:
    <p><b>Proposal:</b> ${ c.event.proposal.title }<br></p>
%endif
    <p><b>Title:</b> ${ c.event.title }<br></p>
    <p><b>URL:</b> ${ c.event.url }<br></p>
    <p><b>Publish:</b> ${ h.yesno(c.event.publish) | n }<br></p>
    <p><b>Exclusive:</b> ${ h.yesno(c.event.exclusive) | n }<br></p>

    <h3>This events schedule</h3>
    <table>
      <thead>
        <tr>
          <th>Time Slot</th>
          <th>Location</th>
%if c.can_edit:
          <th></th>
          <th></th>
%endif
        </tr>
      </thead>
%for schedule in c.event.schedule:
      <tbody>
        <tr>
          <td>${ h.link_to(str(schedule.time_slot.start_time) + ' - ' + str(schedule.time_slot.end_time), url=h.url_for(controller='time_slot', action='view', id=schedule.time_slot.id)) }</td>
          <td>${ h.link_to(schedule.location.display_name, url=h.url_for(controller='location', action='view', id=schedule.location.id)) }</td>
%if c.can_edit:
          <td>${ h.link_to('Edit', url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }</td>
          <td>${ h.link_to('Delete', url=h.url_for(controller='schedule', action='delete', id=schedule.id)) }</td>
%endif
        </tr>
      </tbody>
%endfor
      <tfoot>
        <tr>
          <td colspan='4'>${ h.link_to('Add to schedule', url=h.url_for(controller='schedule', action='new', event=c.event.id)) }</td>
      </tfoot>
    </table>

    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>

