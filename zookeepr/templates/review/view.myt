<h1>Review <% c.review.id %></h1>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<p>
Review by <% c.review.reviewer.fullname %>
</p>

<table>
<tr>
<th>Familiarity</th>
<td><% c.review.familiarity | h %></td>
</tr>

<tr>
<th>Technical</th>
<td><% c.review.technical | h %></td>
</tr>

<tr>
<th>Experience</th>
<td><% c.review.experience | h %></td>
</tr>

<tr>
<th>Coolness</th>
<td><% c.review.coolness | h %></td>
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

