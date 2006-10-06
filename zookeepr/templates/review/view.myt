<h1>Review <% c.review.id %></h1>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<p>
Review by <% c.review.reviewer.fullname %>
</p>

<p>
Proposal Abstract:
<blockquote>
<% h.truncate(c.review.proposal.abstract, 200) %>
</blockquote>
</p>

<p>
<table>
<tr>
<th>Reviewer's Familiarity with Subject</th>
<td>
% if c.review.familiarity == 0:
0 - Abstained
% else:
<% c.review.familiarity | h %>
% #endif
</td>
</tr>

<tr>
<th>Proposer's Technical Rating</th>
<td><% c.review.technical | h %></td>
</tr>

<tr>
<th>Proposer's Speaking Experience Rating</th>
<td><% c.review.experience | h %></td>
</tr>

<tr>
<th>Reviewer's Excitement Level</th>
<td><% c.review.coolness | h %></td>
</tr>

<tr>
<th>Recommended Stream</th>
<td><% c.review.stream.name %></td>
</tr>

</table>
</p>

<p>
Reviewer Comment:
<blockquote>
<% c.review.comment %>
</blockquote>
</p>
