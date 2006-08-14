<h2>List proposals</h2>

<table>

% if len(c.proposal_collection) > 0:
<tr>
<th>Title</th>
<th>Type</th>
<th>Abstract</th>
<th>Experience</th>
<th>URL</th>
<th>Attachment</th>
<th>Person</th>
</tr>
% #endif

% for s in c.proposal_collection:
<tr>
	<td><% h.link_to(s.title, url=h.url(action='view', id=s.id)) %></td>
	<td>
% 	if s.type:
<% s.type.name %>
% 	#endif
</td>
	<td><% str(s.abstract)[:30] %></td>
	<td><% str(s.experience)[:30] %></td>
	<td><% h.link_to(s.url, url=s.url) %></td>
	<td><% str(s.attachment)[:30] %></td>
	<td>
% 	for p in s.people:

<% h.link_to(p.handle or p.id, url=h.url(controller='person', action='view', id=p.id)) %>
%	# endfor
</td>

% 	if c.can_edit:
%		for action in ['edit', 'delete']:
	<td><% h.link_to(action, url=h.url(action=action, id=s.id)) %></td>
%		# endfor
%	#endif
</tr>
% #endfor
</table>


<%python>
#if c.proposal_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.proposal_pages.current.previous)) + '  ')
#if c.proposal_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.proposal_pages.current.next)))

m.write('<br />')
if c.can_edit:
    m.write(h.link_to('New proposal', url=h.url(action='new')))
</%python>
 
