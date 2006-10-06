<h1>Review <% c.review.id %></h1>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<p>
Review by <% c.review.reviewer.fullname %>
</p>

<table>
<tr>
<th>Reviewer Familiarity with Subject</th>
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


<p>
Reviewer Comment:
<blockquote>
<% c.review.comment %>
</blockquote>
</p>


<hr />
<p></p>

<h2>Proposal details</h2>


<p>
This is a proposal for a <% c.review.proposal.type.name %>
submitted at
<% c.review.proposal.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
(last updated at <% c.review.proposal.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>)
</p>

<p>
Project URL:
% if c.review.proposal.url:
<% h.link_to(c.review.proposal.url, url=c.review.proposal.url) %>.
% else:
<em>none given</em>.
% #endif
</p>

<p>Abstract:</p>
<blockquote>
<% h.auto_link(h.simple_format(c.review.proposal.abstract)) %>
</blockquote>
</p>

</p>

<blockquote>
<% h.auto_link(h.simple_format(c.review.proposal.experience)) %>
</blockquote>

