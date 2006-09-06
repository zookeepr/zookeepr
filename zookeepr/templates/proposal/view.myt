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

<div class="attachment">
% if len(c.proposal.attachments) > 0:
#<em>Attachments:</em>
<table>
<caption>Attachments</caption>
<tr>
<th>Filename</th>
<th>Size</th>
<th>Date uploaded</th>
</tr>
% #endif

% for a in c.proposal.attachments:
<tr class="<% h.cycle('even', 'odd') %>">

<td>
<% h.link_to(a.filename, url=h.url_for(controller='attachment', action='view', id=a.id)) %>
</td>

<td>
<% len(a.content) %>b
</td>

<td>
<% a.creation_timestamp.strftime("%Y-%m-%d %H:%M") %>
</td>

</tr>
% #endfor

% if len(c.proposal.attachments) > 0:
</table>
% #endfor
<p>
<% h.link_to('Add an attachment', url=h.url(action='attach')) %>
</p>
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
