% import random
<h2>Proposal List</h2>

<p>
<% h.link_to('Go to your list of reviews', url=h.url(controller='review')) %>
</p>

% if c.num_reviewers <= 0:
%	c.num_reviewers = 1
You have reviewd <% len(c.person.reviews) %> out of your quota of  <% c.num_proposals * 3 / c.num_reviewers %>. 



% for pt in c.proposal_types:
%	collection = getattr(c, '%s_collection' % pt.name)
%	random.shuffle(collection)
%	collection.sort(cmp = lambda x, y: cmp(len(x.reviews), len(y.reviews)))


%	min_reviews = 100
%	for p in collection:
%		if len(p.reviews) < min_reviews:
%			min_reviews = len(p.reviews)
%		elif not p.reviews:
%			min_reviews = 0
%		# endif
%	#endfor

<h2><% pt.name %>s (<% len(collection) %>)</h2>

Proposal cannot be reviewed again untill all proposals have been reviewed at least <% min_reviews +1 %> times;
<table class="list">

<tr>
#<th>#</th>
<th>ID - Title</th>
#<th>Abstract</th>
#<th>Experience</th>
#<th>Project URL</th>
<th>Submitter(s)</th>
<th>Submission Time</th>
<th>Number of reviews</th>
<th>Reviewed?</th>
</tr>

% 	for s in collection:
# don't show the row if we've already reviewed it
%		if not [ r for r in s.reviews if r.reviewer == c.signed_in_person ]:
<tr class="<% h.cycle('even', 'odd') %>">
#	<td><% s.id %></td>
	<td><% h.link_to("%s - %s" % (s.id, h.util.html_escape(s.title)), url=h.url(action='view', id=s.id)) %></td>
#	<td><% h.truncate(s.abstract) %></td>
#	<td><% h.truncate(s.experience) %></td>
#	<td><% h.link_to(h.truncate(s.url), url=s.url) %></td>
	<td>
% 		for p in s.people:

<% h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address or p.id, url=h.url(controller='person', action='view', id=p.id)) %>
%	# endfor
</td>

<td>
<% s.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</td>
<td>
<% len(s.reviews) %>
</td>

	<td>
%		if min_reviews < 3 and len(s.reviews) > min_reviews :
	<small>Review something with <% min_reviews %> reviews first;
	<% h.link_to("review anyway", url=h.url(action="review", id=s.id)) %>
	</small>
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
%		#endif only unreviewed
% 	#endfor collection
</table>

<br>

% #endfor proposal types

<%python>
#if c.proposal_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.proposal_pages.current.previous)) + '  ')
#if c.proposal_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.proposal_pages.current.next)))

#m.write('<br>')
#if c.can_edit:
#    m.write(h.link_to('New proposal', url=h.url(action='new')))
</%python>
 

<%method title>
Proposals - <& PARENT:title &>
</%method>
