<div id="menu">

<ul>

<li>
% if r.environ.has_key('REMOTE_USER'):
<% h.link_to('sign out', url=h.url(controller='account', action='signout')) %>
% else:
<% h.link_to('sign in', url=h.url(controller='account', action='signin')) %>
% #endif
</li>

<li><% h.link_to('about', url=h.url(controller='about', action='index')) %></li>
<li><% h.link_to('press', url=h.url(controller='about', action='press')) %></li>
<li><% h.link_to('sydney', url=h.url(controller='about', action='sydney')) %></li>
<li><% h.link_to('contact', url=h.url(controller='about', action='contact')) %></li>
<li class="last"><% h.link_to('sponsors', url=h.url(controller='about', action='sponsors')) %></li>
</ul>

</div>
