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
at
<% c.proposal.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
(last updated at <% c.proposal.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>)
</p>

<div class="abstract">
<p>
<em>Abstract</em>
</p>
<blockquote>
<% c.proposal.abstract | h, s, l %>
</blockquote>
</div>

% if c.proposal.url:
<p class="url">
# FIXME: I reckon this should go into the helpers logic
%	if '://' in c.proposal.url:
<% h.link_to(c.proposal.url, url=c.proposal.url) %>
%	else:
<% h.link_to(c.proposal.url, url='http://' + c.proposal.url) %>
%	#endif
</p>
% #endif

<div class="experience">
<p>
<em>Speaking experience:</em>
</p>
<blockquote>
% if c.proposal.experience:
<% c.proposal.experience | h, s, l %>
% else:
[none provided]
% #endif
</blockquote>
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
<% h.number_to_human_size(len(a.content)) %>
</td>

<td>
<% a.creation_timestamp.strftime("%Y-%m-%d %H:%M") %>
</td>

<td>
<% h.link_to('delete', url=h.url(controller='attachment', action='delete', id=a.id)) %>
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

% if c.signed_in_person in c.proposal.people:
<li>
<% h.link_to('Edit', url=h.url(action='edit',id=c.proposal.id)) %>
</li>
% #endif

% if 'reviewer' in [x.name for x in c.signed_in_person.roles]:
<li>
<% h.link_to('Review this proposal', url=h.url(action='review')) %>
</li>
% #endif

</ul>
</p>

</div>

<div id="wiki">
<% h.wiki_here() %>
</div>

<%method title>
<% h.truncate(c.proposal.title) %> - <% c.proposal.type.name %> proposal - <& PARENT:title &>
</%method>
