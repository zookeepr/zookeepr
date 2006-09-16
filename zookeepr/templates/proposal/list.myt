<h2>List of Proposals</h2>


% for pt in c.proposal_types:
%	collection = getattr(c, '%s_collection' % pt.name)
<h3><% pt.name %>s (<% len(collection) %>)</h3>

<table>

<tr>
<th>#</th>
<th>Title</th>
#<th>Abstract</th>
#<th>Experience</th>
#<th>Project URL</th>
<th>Submitter(s)</th>
<th>Reviewed?</th>
</tr>

% 	for s in collection:
<tr class="<% h.cycle('even', 'odd') %>">
	<td><% s.id %></td>
	<td><% h.link_to(h.util.html_escape(s.title), url=h.url(action='view', id=s.id)) %></td>
#	<td><% h.truncate(s.abstract) %></td>
#	<td><% h.truncate(s.experience) %></td>
#	<td><% h.link_to(h.truncate(s.url), url=s.url) %></td>
	<td>
% 		for p in s.people:

<% h.link_to(p.fullname or p.email_address or p.id, url=h.url(controller='person', action='view', id=p.id)) %>
%	# endfor
</td>
	<td>
%		if [ r for r in s.reviews if r.reviewer == c.signed_in_person ]:
	TICK!
%		else:
	<% h.link_to("Review now!", url=h.url(action="review", id=s.id)) %>
%		#ENDIF
	</td>
#% 	if c.can_edit:
#%		for action in ['edit', 'delete']:
#	<td><% h.link_to(action, url=h.url(action=action, id=s.id)) %></td>
#%		# endfor
#%	#endif
</tr>
% 	#endfor collection
</table>

<br />

% #endfor proposal types

<%python>
#if c.proposal_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.proposal_pages.current.previous)) + '  ')
#if c.proposal_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.proposal_pages.current.next)))

#m.write('<br />')
#if c.can_edit:
#    m.write(h.link_to('New proposal', url=h.url(action='new')))
</%python>
 

<%method title>
Proposals - <& PARENT:title &>
</%method>
