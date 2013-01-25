<%inherit file="/base.mako" />

<h2>List Fulfilment Group</h2>

% if len(c.fulfilment_group_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Person</th>
    <th>Code</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for fulfilment_group in c.fulfilment_group_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(fulfilment_group.id, url=h.url_for(action='view', id=fulfilment_group.id)) }</td>
    <td>
%     if fulfilment_group.person:
      ${ h.link_to(fulfilment_group.person.fullname, url=h.url_for(controller='person', action='view', id=fulfilment_group.person_id)) }
%     endif
    </td>
    <td>${ fulfilment_group.code }</td>
%     if c.can_edit:
%       for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=fulfilment_group.id)) }</td>
%       endfor
%     endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Fulfilment Group', url=h.url_for(action='new')) }</p>
% endif
 
