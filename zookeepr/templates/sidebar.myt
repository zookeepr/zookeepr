<div class="sidebarbox">

% if r.environ.has_key('REMOTE_USER'):
<p>
logged in as <% h.link_to(r.environ['REMOTE_USER'], url=h.url(controller='person', action='view', id=r.environ['REMOTE_USER'])) %>.
<% h.link_to('sign out', url=h.url(controller='/security', action='signout')) %>
</p>
% #endif

<p><% h.link_to('Register now!', url=h.url(controller='register')) %></p>

<ul>
<li><% h.link_to('Call for Participation open', h.url(controller='cfp')) %>
<p>June 1, 2006</p>
</li>
<li><% h.link_to('Register for the conference', h.url(controller='register')) %>
<p>September 3, 2006</p>
</li>
</ul>
</div>
