<h1>Profile of <% c.profile.fullname |h %></h1>

% content = h.wiki_fragment('/profile/%d' % c.profile.id)
% if 'This page does not exist yet.' in content:
%	if len(c.profile.proposals) > 0:
%		content = c.profile.proposals[0].experience
%	else:
%		content = None
%	#endif
% #endif
% if content:
<div id="bio">
<p><% content %></p>
</div>
% #endif

<div id="talks">
<h2>Talks</h2>
<table>
% for p in c.profile.proposals:
<tr class="<% h.cycle('even', 'odd') %>">

<td><% h.link_to(p.title, url=h.url(controller='talk', action='view', id=p.id)) %></td>

</tr>
% #endif
</table>
</div>

<%method title>
<% c.profile.handle |h %> profile - <& PARENT:title &>
</%method>
