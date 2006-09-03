<table>
<tr>
<th>#</th>
<th>Proposal title</th>
<th>Reviewer</th>
<th>Score</th>
</tr>
% for r in c.review_collection:

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
put scores here
</td>

</tr>

% #endif
</table>
