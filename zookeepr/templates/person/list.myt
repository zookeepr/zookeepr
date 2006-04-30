List persons

(<a href="<% h.url_for(action='new') %>">new person</a>)


<table>

% if len(c.persons) > 0:
<tr>
<th>Name</th>
</tr>
% #endif

% for p in c.persons:
<tr>

%	for key in ['name']:
<td><a href="<% h.url_for(action='view', id=p.handle) %>"><% p.handle %></a></td>
%	#endfor

%	for action in ['view', 'edit', 'delete']:
<td><a href="<% h.url_for(action=action, id=p.handle) %>"><% action %></a></td>
%	#endfor

</tr>
% #endfor

</table>

