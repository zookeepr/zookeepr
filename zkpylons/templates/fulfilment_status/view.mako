<%inherit file="/base.mako" />

    <h2>View Fulfilment Status</h2>

    <p><b>Name:</b> ${ c.fulfilment_status.name }<br></p>
    <p>
      <b>Void:</b> ${ h.yesno(c.fulfilment_status.void) |n }<br />
      <sub>Does this status mark the Fulfilment void</sub>
    </p>
    <p>
      <b>Completed:</b> ${ h.yesno(c.fulfilment_status.completed) |n }<br />
      <sub>Does this status mark the Fulfilment completed</sub>
    </p>
    <p>
      <b>Locked:</b> ${ h.yesno(c.fulfilment_status.locked) |n }<br />
      <sub>Does this status mark the Fulfilment locked</sub>
    </p>
    <p><b>Fulfilment Types this status can be used with:</b></p>
    <table>
      <tr>
        <th>#</th>
        <th>Name</th>
      </tr>
% for type in c.fulfilment_status.types:
      <tr>
        <td>${ h.link_to(type.id, h.url_for(controller='fulfilment_type', action='view', id=type.id))}</td>
        <td>${ type.name }</td>
      </tr>
% endfor
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
