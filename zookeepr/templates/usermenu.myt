<br>
<ul id="usermenu" class="menu">

% if 'signed_in_person_id' in session:

<li>
signed in
# as <% c.signed_in_person.email_address %>
</li>

#<li>
#<% h.link_to('my home', url=h.url(controller='profile', action='index')) %>
#</li>

<li>
<% h.link_to('my profile', url=h.url(controller='profile', action='view', id=session['signed_in_person_id'])) %>
</li>

<li>
<% h.link_to('sign out', url=h.url(controller='person', action='signout_confirm')) %>
</li>

% else:

<li>
<% h.link_to('sign in', url=h.url(controller='person', action='signin')) %>
</li>

<li>
<% h.link_to('new user?', url=h.url(controller='person', action='new')) %>
</li>

% #endif
</ul>
