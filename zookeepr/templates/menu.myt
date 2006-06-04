<div id="menu">

<ul>

<li>
% if r.environ.has_key('REMOTE_USER'):
<% h.link_to('sign out', url=h.url(controller='account', action='signout')) %>
% else:
<% h.link_to('sign in', url=h.url(controller='account', action='signin')) %>
% #endif
</li>

<li><% h.link_to("what's on?", url=h.url(controller='about', action='view', id='whatson')) %></li>
<li><% h.link_to('programme', url=h.url(controller='about', action='view', id='programme')) %></li>
<li><% h.link_to('dates', url=h.url(controller='about', action='view', id='dates')) %></li>
<li><% h.link_to('press', url=h.url(controller='about', action='view', id='press')) %></li>
<li><% h.link_to('sydney', url=h.url(controller='about', action='view', id='sydney')) %></li>
<li><% h.link_to('contact', url=h.url(controller='about', action='view', id='contact')) %></li>
<li><% h.link_to('sponsors', url=h.url(controller='about', action='view', id='sponsors')) %></li>
<li class="last"><% h.link_to('home', url=h.url('home')) %></li>
</ul>

</div>
