<h1>Review <% c.review.id %></h1>

<div class="contents"><h3>Review Pages</h3>
<ul>
<li><a href="/review/help">How to review</a></li>
<li><% h.link_to('Review proposals', url=h.url(controller='proposal', action='review_index')) %></li>
<li><% h.link_to('Your reviews', url=h.url(controller='review', action='index')) %></li>
<li><% h.link_to('Summary of proposals', url=h.url(controller='proposal', action='summary')) %></li>
<li><% h.link_to('Reviewer summary', url=h.url(controller='review', action='summary')) %></li>
</ul>
</div>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<p>
<b>Review by:</b> <% c.review.reviewer.firstname %> <% c.review.reviewer.lastname %>
</p>

<p>
<b>Proposal Abstract:</b>  (<% h.link_to('go to this proposal', url=h.url(controller='proposal', action='review', id=c.review.proposal.id)) %>)
</p>
<blockquote>
<p><% h.truncate(c.review.proposal.abstract, 200) | h%></p>
</blockquote>

<br />
<p><b>Score:</b> <% c.review.score | h %></p>
<p><b>Recommended Stream:</b> <% c.review.stream.name | h %></p>
% if c.review.proposal.proposal_type_id is not 2:
<p><b>Recommended Miniconf:</b><% c.review.miniconf | h %></p>
% #endif

<p><b>Reviewer Comment:</b></p>
<blockquote>
<p><% c.review.comment | h%></p>
</blockquote>
