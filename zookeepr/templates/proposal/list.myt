<h2>List proposals</h2>

<table>

% if len(c.proposal_collection) > 0:
<tr>
<th>#</th>
<th>Title</th>
<th>Type</th>
#<th>Abstract</th>
#<th>Experience</th>
#<th>Project URL</th>
<th>Person</th>
</tr>
% #endif

% for s in c.proposal_collection:
<tr class="<% h.cycle('even', 'odd') %>">
	<td><% h.counter() %></td>
	<td><% h.link_to(s.title, url=h.url(action='view', id=s.id)) %></td>
	<td>
% 	if s.type:
<% s.type.name %>
% 	#endif
</td>
#	<td><% h.truncate(s.abstract) %></td>
#	<td><% h.truncate(s.experience) %></td>
#	<td><% h.link_to(h.truncate(s.url), url=s.url) %></td>
	<td>
% 	for p in s.people:

<% h.link_to(p.fullname or p.email_address or p.id, url=h.url(controller='person', action='view', id=p.id)) %>
%	# endfor
</td>

#% 	if c.can_edit:
#%		for action in ['edit', 'delete']:
#	<td><% h.link_to(action, url=h.url(action=action, id=s.id)) %></td>
#%		# endfor
#%	#endif
</tr>
% #endfor
</table>


<%python>
#if c.proposal_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.proposal_pages.current.previous)) + '  ')
#if c.proposal_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.proposal_pages.current.next)))

#m.write('<br />')
#if c.can_edit:
#    m.write(h.link_to('New proposal', url=h.url(action='new')))
</%python>
 
