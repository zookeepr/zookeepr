<%flags>
	inherit="/layout.myt"
</%flags>

List submission types

(<a href="<% h.url_for(action='new') %>">new submission type</a>)


<table>

% if len(c.submissiontypes) > 0:
<tr>
<th>Name</th>
</tr>
% #endif

% for st in c.submissiontypes:
<tr>

%	for key in ['name']:
<td><a href="<% h.url_for(action='view', id=st.id) %>"><% st.name %></a></td>
%	#endfor

%	for action in ['view', 'edit', 'delete']:
<td><a href="<% h.url_for(action=action, id=st.id) %>"><% action %></a></td>
%	#endfor

</tr>
% #endfor

</table>

