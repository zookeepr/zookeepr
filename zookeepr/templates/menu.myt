<div id="menu">

<p id="account">
% if r.environ.has_key('REMOTE_USER'):
logged in as <% h.link_to(r.environ['REMOTE_USER'], url=h.url(controller='person', action='view', id=r.environ['REMOTE_USER'])) %>,
<% h.link_to('sign out', url=h.url(controller='security', action='signout')) %>
% else:
<% h.link_to('sign in', url=h.url(controller='security', action='signin')) %>
% #endif
</p>

<ul>
<li><% h.link_to("what's on?") %></li>
<li><% h.link_to('programme') %></li>
<li><% h.link_to('dates') %></li>
<li><% h.link_to('press') %></li>
<li><% h.link_to('sydney') %></li>
<li><% h.link_to('contact') %></li>
<li><% h.link_to('sponsors') %></li>
<li class="last"><% h.link_to('home', url=h.url('home')) %></li>
</ul>

</div>
