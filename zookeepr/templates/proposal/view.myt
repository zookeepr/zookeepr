<h2><% c.proposal.title | h %></h2>

<div id="proposal">

<p class="submitted">
Proposal for a
<% c.proposal.type.name %> 
submitted by
% for p in c.proposal.people:
<% p.fullname %>
&lt;<% p.email_address %>&gt;
% #endfor
</p>

<div class="abstract">
<% h.auto_link(h.simple_format(c.proposal.abstract)) %>
</div>

% if c.proposal.url:
<p class="url">
<% h.link_to(c.proposal.url, url=c.proposal.url) %>
</p>
% #endif

<div class="experience">
<em>Speaking experience:</em>
% if c.proposal.experience:
<br />
<% h.auto_link(h.simple_format(c.proposal.experience)) %>
% else:
[none provided]
% #endif
</div>

<hr />

<p class="actions">
<ul>

% if c.person in c.proposal.people:
<li>
<% h.link_to('Edit', url=h.url(action='edit',id=c.proposal.id)) %>
</li>
% #endif

% if 'reviewer' in [x.name for x in c.person.roles]:
<li>
<% h.link_to('Review this proposal', url=h.url(action='review')) %>
</li>
% #endif

</ul>
</p>

</div>

<%method title>
<% h.truncate(c.proposal.title) %> - <% c.proposal.type.name %> proposal - <& PARENT:title &>
</%method>
