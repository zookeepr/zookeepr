<div id="menu">

<ul>

% if session.has_key('username'):
<li><% h.link_to(session['username'], url=h.url(controller='person', action='view', id=session['username'])) %></li>
% else:
<li><% h.link_to('sign in', url=h.url(controller='security', action='signin')) %></li>
% #endif

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
