<h2>Reviews</h2>

<table>
<tr>
<th>#</th>
<th>Proposal title</th>
<th>Reviewer</th>
<th>Familiarity</th>
<th>Tech Content</th>
<th>Speaker Exp</th>
<th>Coolness</th>
<th>Stream</th>
<th>Comment</th>
</tr>
% for r in c.review_collection:
# only see the review if you wrote it
%	if r.reviewer == c.signed_in_person:

<tr class="<% h.cycle('even', 'odd') %>">

<td>
<% h.counter() %>
</td>

<td>
<% r.proposal.title %>
</td>

<td>
<% r.reviewer.fullname %>
</td>

<td>
<% r.familiarity |h %>
</td>

<td>
<% r.technical |h %>
</td>

<td>
<% r.experience |h %>
</td>

<td>
<% r.coolness |h %>
</td>

<td>
<% r.stream.name |h %>
</td>

<td>
<% h.truncate(r.comment) %>
</td>

</tr>

% 	#endif only look at own reviews
% #endfor
</table>

<%method title>
Reviews - <& PARENT:title &>
</%method>
