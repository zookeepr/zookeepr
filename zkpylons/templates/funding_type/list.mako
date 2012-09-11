<%inherit file="/base.mako" />

<h2>List funding types</h2>

<table>

% if len(c.funding_type_collection) > 0:
  <tr>
    <th>Name</th>
    <th>Active</th>
    <th>Notify Email</th>
    <th>&nbsp;</th>
  </tr>
% endif

% for st in c.funding_type_collection:
  <tr>
    <td>${ h.link_to(st.name, url=h.url_for(action='view', id=st.id)) }</td>
    <td>${ h.yesno(st.active) | n }</td>
    <td>${ st.notify_email | h }</td>
    <td>
%   for action in ['edit', 'delete']:
        ${ h.link_to(action, url=h.url_for(action=action, id=st.id)) }
%   endfor
    </td>
  </tr>
% endfor
</table>

<p>${ h.link_to('New funding type', url=h.url_for(action='new')) }</p>
 
