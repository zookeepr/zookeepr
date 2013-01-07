<%inherit file="/base.mako" />

    <h2>View Fulfilment Group</h2>

    <p><b>Person:</b> ${ c.fulfilment_group.person.fullname() }<br></p>
    <p>
      <b>Code:</b> ${ c.fulfilment_group.code }<br />
    </p>
    <p><b>Fulfilments that are part of this group:</b></p>
    <table>
      <tr>
        <th>#</th>
        <th>Person</th>
        <th>Type</th>
        <th>Status</th>
      </tr>
% for fulfilment in c.fulfilment_group.fulfilments:
      <tr>
        <td>${ h.link_to(fulfilment.id, h.url_for(controller='fulfilment_type', action='view', id=fulfilment.id)) }</td>
        <td>${ h.link_to(fulfilment.person.fullname(), h.url_for(controller='person', action='view', id=fulfilment.person_id)) }</td>
        <td>${ fulfilment.type.name }</td>
        <td>${ fulfilment.status.name }</td>
      </tr>
% endfor
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
