<ul id="usermenu" class="linkmenu">

% if c.person:
<li><% h.link_to('my profile', url=h.url(controller='person', action='view', id=c.person.id)) %></li>
<li><% h.link_to('sign out', url=h.url(controller='account', action='signout', id=None)) %></li>
% else:
<li><% h.link_to('sign in', url=h.url(controller='account', action='signin', id=None)) %></li>
% #endif
</ul>
