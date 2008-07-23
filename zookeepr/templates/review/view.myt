<h1>Review <% c.review.id %></h1>

<div class="contents"><h3>Review Pages</h3>
<ul>
<li><% h.link_to('Go to your list of reviews', url=h.url(controller='review')) %></li>
<li><% h.link_to('Go to the summary of proposals', url=h.url(controller='proposal', action='summary')) %></li>
<li><% h.link_to('Go to reviewer summary', url=h.url(controller='review', action='summary')) %></li>
<li><% h.link_to('Review some papers', url=h.url(controller='proposal', action='review_index')) %></li>
</ul>
</div>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<p>
Review by <% c.review.reviewer.firstname %> <% c.review.reviewer.lastname %>
</p>

<p>
Proposal Abstract:  (<% h.link_to('go to this proposal', url=h.url(controller='proposal', action='review', id=c.review.proposal.id)) %>)
</p>
<blockquote>
<p><% h.truncate(c.review.proposal.abstract, 200) | h%></p>
</blockquote>

<br />
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

<p>
Reviewer Comment:
</p>
<blockquote>
<p><% c.review.comment | h%></p>
</blockquote>
