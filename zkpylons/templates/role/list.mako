<%inherit file="/base.mako" />

<h1>List Roles</h1>

<table>

% if len(c.role_collection) > 0:
<tr>
<th>Name</th>
<th>Pretty Name</th>
<th>Comment</th>
<th></th>
<th></th>
</tr>
% endif

% for st in c.role_collection:
<tr>
<tr class="${ h.cycle('odd', 'even') }">
        <td>${ h.link_to(st.name, url=h.url_for(action='view', id=st.id)) }</td>
        <td>
%   if st.pretty_name is not None:
        ${ h.link_to(st.pretty_name, url=h.url_for(action='view', id=st.id)) }
%   else:
        &nbsp;
%   endif
        </td>
        <td>${ st.comment }</td>
%       for action in ['edit', 'delete']:
        <td>${ h.link_to(action, url=h.url_for(action=action, id=st.id)) }</td>
%       endfor
</tr>
% endfor
</table>


<p> ${h.link_to('New role', url=h.url_for(action='new'))} </p>
 
