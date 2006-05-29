<div id="menu">

<ul>

<li>
% if r.environ.has_key('REMOTE_USER'):
<% h.link_to('sign out', url=h.url(controller='account', action='signout')) %>
% else:
<% h.link_to('sign in', url=h.url(controller='account', action='signin')) %>
% #endif
</li>

<li><% h.link_to("what's on?", url=h.url(controller='info', action='whatson')) %></li>
<li><% h.link_to('programme', url=h.url(controller='info', action='programme')) %></li>
<li><% h.link_to('dates', url=h.url(controller='info', action='dates')) %></li>
<li><% h.link_to('press', url=h.url(controller='info', action='press')) %></li>
<li><% h.link_to('sydney', url=h.url(controller='info', action='sydney')) %></li>
<li><% h.link_to('contact', url=h.url(controller='info', action='contact')) %></li>
<li><% h.link_to('sponsors', url=h.url(controller='info', action='sponsors')) %></li>
<li class="last"><% h.link_to('home', url=h.url('home')) %></li>
</ul>

</div>
