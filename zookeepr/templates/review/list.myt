<p>
<% h.link_to('Go to your unreviewed proposals', url=h.url(controller='proposal', action='review_index', id=None)) %>
</p>

<h2>Reviews</h2>

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

<p>
<% h.link_to('Go to your unreviewed proposals', url=h.url(controller='proposal', action='review_index', id=None)) %>
</p>

<%method title>
Reviews - <& PARENT:title &>
</%method>
