<h1>List submissions</h1>

<table>

% if len(c.submission_collection) > 0:
<tr>
<th>Title</th>
<th>Type</th>
<th>Abstract</th>
<th>Experience</th>
<th>URL</th>
<th>Person</th>
</tr>
% #endif

% for s in c.submission_collection:
<tr>
	<td><% h.link_to(s.title, url=h.url(action='view', id=s.id)) %></td>
	<td>
% 	if s.submission_type:
<% s.submission_type.name %>
%	#endif
</td>
	<td><% str(s.abstract)[:30] %></td>
	<td><% str(s.experience)[:30] %></td>
	<td><% h.link_to(s.url) %></td>
	<td>
% 	if s.person:
<% h.link_to(s.person.handle, url=h.url(controller='person', action='view', id=s.person.handle)) %>
%	# endif
</td>

% 	if c.can_edit:
%		for action in ['edit', 'delete']:
	<td><% h.link_to(action, url=h.url(action=action, id=s.id)) %></td>
%		# endif
%	 #endfor
</tr>
% #endfor
</table>


<%python>
#if c.submission_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.submission_pages.current.previous)) + '  ')
#if c.submission_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.submission_pages.current.next)))

m.write('<br />')
if c.can_edit:
    m.write(h.link_to('New submission', url=h.url(action='new')))
</%python>
 