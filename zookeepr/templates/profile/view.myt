<h1>Profile</h1>

<div>
<% c.profile.fullname |h %>
</div>

<div id="wiki">
<% h.wiki_fragment('/profile/%d' % c.profile.id) %>
</div>

<div id="proposals">
<h2>Proposals</h2>
<table>
% for p in c.profile.proposals:
<tr class="<% h.cycle('even', 'odd') %>">

<td><% h.link_to(p.title, url=h.url(controller='talk', id=p.id)) %></td>

</tr>
% #endif
</table>
</div>

<%method title>
<% c.profile.handle |h %> profile - <& PARENT:title &>
</%method>
