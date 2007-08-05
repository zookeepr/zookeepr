<h1>Review <% c.review.id %></h1>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<p>
Review by <% c.review.reviewer.firstname %> <% c.review.reviewer.lastname %>
</p>

<p>
Proposal Abstract:  (<% h.link_to('go to this proposal', url=h.url(controller='proposal', action='view', id=c.review.proposal.id)) %>)
<blockquote>
<% h.truncate(c.review.proposal.abstract, 200) | h%>
</blockquote>
</p>

<p>
<table>
<tr>
<th>Score</th>
<td><% c.review.score | h %></td>
</tr>

<tr>
<th>Recommended Stream</th>
<td><% c.review.stream.name | h %></td>
</tr>

<tr>
<th>Recommended Miniconf</th>
<td><% c.review.miniconf | h %></td>
</tr>

</table>
</p>

<p>
Reviewer Comment:
<blockquote>
<% c.review.comment | h%>
</blockquote>
</p>
