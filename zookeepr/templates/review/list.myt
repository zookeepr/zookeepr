<h2>Your reviews</h2>

<div class="contents"><h3>Review Pages</h3>
<ul>
<li><% h.link_to('Go to your unreviewed proposals', url=h.url(controller='proposal', action='review_index')) %></li>
<li><% h.link_to('Go to the summary of proposals', url=h.url(controller='proposal', action='summary')) %></li>
<li><% h.link_to('Go to reviewer summary', url=h.url(controller='review', action='summary')) %></li>
</ul>
</div>

<table>
<tr>
<th>#</th>
<th>Proposal title</th>
<th>Reviewer</th>
<th>Score</th>
<th>Stream</th>
<th>Comment</th>
<th>Edit</th>
</tr>
% for r in c.review_collection:
# only see the review if you wrote it
%	if r.reviewer == c.signed_in_person:

<tr class="<% h.cycle('even', 'odd') %>">

<td>
<% h.counter() %>
</td>

<td>
<% h.link_to("%s - %s" % (r.proposal.id, r.proposal.title), url=h.url(controller='review', action='edit', id=r.id)) %>
</td>

<td>
<% r.reviewer.firstname %>
<% r.reviewer.lastname %>
</td>

<td>
<% r.score |h %>
</td>

<td>
<% r.stream.name |h %>
</td>

<td>
<% h.truncate(r.comment) %>
</td>

<td>
<% h.link_to("edit", url=h.url(controller='review', action='edit', id=r.id)) %>
</td>
</tr>

% 	#endif only look at own reviews
% #endfor
</table>

<%method title>
Reviews - <& PARENT:title &>
</%method>
