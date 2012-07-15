<%inherit file="/base.mako" />

<h2>List proposal types</h2>

<table>

% if len(c.proposal_type_collection) > 0:
  <tr>
    <th>Name</th>
    <th>Notify Email</th>
    <th>&nbsp;</th>
  </tr>
% endif

% for st in c.proposal_type_collection:
  <tr>
    <td>${ h.link_to(st.name, url=h.url_for(action='view', id=st.id)) }</td>
    <td>${ st.notify_email }</td>
%   for action in ['edit', 'delete']:
    <td>${ h.link_to(action, url=h.url_for(action=action, id=st.id)) }</td>
%   endfor
  </tr>
% endfor
</table>

<p>${ h.link_to('New proposal type', url=h.url_for(action='new')) }</p>
 
