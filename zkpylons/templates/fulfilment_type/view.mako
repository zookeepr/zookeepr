<%inherit file="/base.mako" />

    <h2>View Fulfilment Type</h2>

    <p><b>Name:</b> ${ c.fulfilment_type.name }<br></p>
    <p><b>Fulfilment Status this Type can be used with:</b></p>
    <table>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Void</th>
        <th>Completed</th>
      </tr>
% for status in c.fulfilment_type.status:
      <tr>
        <td>${ h.link_to(status.id, h.url_for(controller='fulfilment_status', action='view', id=status.id))}</td>
        <td style="text-align: center;">${ status.name }</td>
        <td style="text-align: center;">${ h.yesno(status.void) |n }</td>
        <td style="text-align: center;">${ h.yesno(status.completed) |n }</td>
      </tr>
% endfor
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
