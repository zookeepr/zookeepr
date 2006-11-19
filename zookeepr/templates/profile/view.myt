<h1><% c.profile.fullname |h %></h1>

# Show personal details
% if 'signed_in_person_id' in session and session['signed_in_person_id'] == c.profile.id:
<p>
email address: <% c.profile.email_address %>
</p>
<p>
display name: <% c.profile.handle %>
</p>
<p>
first name: <% c.profile.firstname %>
</p>
<p>
last name: <% c.profile.lastname %>
</p>
<p>
phone: <% c.profile.phone %>
</p>

%	if c.profile.registration:
<p>
address: <% c.profile.registration.address1 %>
<br />
<% c.profile.registration.address2 %>
</p>

<p>
city/suburb: <% c.profile.registration.city %>
</p>

<p>
state/province: <% c.profile.registration.state %>
</p>

<p>
country: <% c.profile.registration.country %>
</p>

%	else:
<p>
You haven't yet registered for the conference.  <% h.link_to('Register now!', url=h.url('/Registration')) %>
</p>
%	#endif

% #endif

% if len(c.profile.accepted_talks) > 0:
<%python>
content = h.wiki_fragment('/wiki/profile/%d' % c.profile.id)

if 'This page does not exist yet.' in content:
	if len(c.profile.proposals) > 0:
		content = c.profile.proposals[0].experience
	else:
		content = None
</%python>
% if content:
<div id="bio">
<p><% content |s %></p>
</div>
% #endif

<div id="talks">
<h2>Talks</h2>
<table>
%	for p in c.profile.accepted_talks:
<tr class="<% h.cycle('even', 'odd') %>">

<td><% h.link_to(p.title, url=h.url(controller='talk', action='view', id=p.id)) %></td>

</tr>
%	#endif
</table>
</div>
% #endif

<%method title>
profile - <& PARENT:title &>
</%method>
