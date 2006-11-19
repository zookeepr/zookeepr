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

%	if c.profile.registration:
<hr />

<p>
ticket: <% c.profile.registration.type %>
</p>

<hr />

<p>
company: <% c.profile.registration.company %>
</p>

<p>
address: <% c.profile.registration.address1 %>
<br />
<% c.profile.registration.address2 %>
</p>

<p>
city/suburb: <% c.profile.registration.city %>
</p>

<p>
postcode: <% c.profile.registration.postcode %>
</p>

<p>
state/province: <% c.profile.registration.state %>
</p>

<p>
country: <% c.profile.registration.country %>
</p>

<p>
phone: <% c.profile.registration.phone %>
</p>

<hr />

<p>
shell:
%		if c.profile.registration.shelltext:
<% c.profile.registration.shelltext %>
%		else:
<% c.profile.registration.shell %>
%		#endif
</p>

<p>
editor:
%		if c.profile.registration.editortext:
<% c.profile.registration.editortext %>
%		else:
<% c.profile.registration.editor %>
%		#endif
</p>

<p>
distro:
%		if c.profile.registration.distrotext:
<% c.profile.registration.distrotext %>
%		else:
<% c.profile.registration.distro %>
%		#endif
</p>

<p>
description: <% c.profile.registration.silly_description %>
</p>

<p>
teesize: <% c.profile.registration.teesize %>
</p>

<p>
Additional dinner tickets: <% c.profile.registration.dinner %>
</p>

<p>
Dietary requirements: <% c.profile.registration.diet %>
</p>

<p>
Special requirements: <% c.profile.registration.special %>
</p>

<p>
Number of people you've invited to Open Day: <% c.profile.registration.opendaydrag %>
</p>

<hr />

<p>
Partner's email address: <% c.profile.registration.partner_email %>
</p>

<p>
Kids coming: aged 0-3: <% c.profile.registration.kids_0_3 %>; 4-6: <% c.profile.registration.kids_4_6 %>; 7-9: <% c.profile.registration.kids_7_9 %>; 10+: <% c.profile.registration.kids_10 %>
</p>

<hr />

<p>
Accommodation: <% c.profile.registration.accommodation.name %>
</p>

<p>
check-in date: <% c.profile.registration.checkin %>
</p>

<p>
check-out date: <% c.profile.registration.checkout %>
</p>

<hr />

<p>
join the LA: <% c.profile.registration.lasignup %>
</p>

<p>
Join the conference announcement list: <% c.profile.registration.announcesignup %>
</p>

<p>
Join the delegates discussion list: <% c.profile.registration.delegatesignup %>
</p>

<hr />

<p>
Previous miniconfs: <% c.profile.registration.prevlca %>
</p>

<p>
Miniconfs likely to attend: <% c.profile.registration.miniconf %>
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
