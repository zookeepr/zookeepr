<%inherit file="/base.mako" />

<h1>List roles</h1>

<table>

% if len(c.role_collection) > 0:
<tr>
<th>Name</th>
<th></th>
<th></th>
</tr>
% endif

% for st in c.role_collection:
<tr>
        <td>${ h.link_to(st.name, url=h.url_for(action='view', id=st.id)) }</td>
%       for action in ['edit', 'delete']:
        <td>${ h.link_to(action, url=h.url_for(action=action, id=st.id)) }</td>
%       endfor
</tr>
% endfor
</table>


<p> ${h.link_to('New role', url=h.url_for(action='new'))} </p>
 
