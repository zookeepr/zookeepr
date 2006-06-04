<div class="sidebarbox">
<div class="contentboxR">
<div class="contentboxC" id="sidebarboxTL"></div>
<div class="contentboxC" id="sidebarboxTR"></div>
</div>

<div class="sidebarcontent">
% if r.environ.has_key('REMOTE_USER'):
<p>
logged in as <% h.link_to(r.environ['REMOTE_USER'], url=h.url(controller='person', action='view', id=r.environ['REMOTE_USER'])) %>.
<% h.link_to('sign out', url=h.url(controller='/account', action='signout')) %>
</p>
% #endif


<ul>
<li><% h.link_to('Sign up', url=h.url(controller='person', action='new')) %></li>
<li><% h.link_to('Call for Participation', h.url(controller='about', action='cfp')) %></li>
<li><% h.link_to('Submit a proposal', h.url(controller='submission', action='new')) %></li>
</ul>
</div>

<div class="contentboxR" id="sidebarboxB">
<div class="contentboxC" id="sidebarboxBL"></div>
<div class="contentboxC" id="sidebarboxBR"></div>
</div>
</div>
