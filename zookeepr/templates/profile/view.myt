<p>
<% c.profile.fullname |h %>'s profile
</p>

<div id="bio">
<p>Bio:</p>
<p>
% content = h.wiki_fragment('/profile/%d' % c.profile.id)
% if 'This page does not exist yet.' in content:
<% c.profile.proposals[0].experience %>
% else:
<% content %>
% #endif
</p>
</div>

<div id="proposals">
<h2>Proposals</h2>
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
