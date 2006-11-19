<h1><% c.profile.fullname |h %></h1>

# Show personal details
% if 'signed_in_person_id' in session and session['signed_in_person_id'] == c.profile.id:
<p>
email address: <% c.profile.email_address |h %>
</p>
<p>
display name: <% c.profile.handle |h %>
</p>
<p>
first name: <% c.profile.firstname |h %>
</p>
<p>
last name: <% c.profile.lastname |h %>
</p>

%	if c.profile.registration:
<hr />

<p>
ticket: <% c.profile.registration.type |h %>
</p>

<hr />

<p>
company: <% c.profile.registration.company |h %>
</p>

<p>
address: <% c.profile.registration.address1 |h %>
<br />
<% c.profile.registration.address2 |h %>
</p>

<p>
city/suburb: <% c.profile.registration.city |h %>
</p>

<p>
postcode: <% c.profile.registration.postcode |h %>
</p>

<p>
state/province: <% c.profile.registration.state |h %>
</p>

<p>
country: <% c.profile.registration.country |h %>
</p>

<p>
phone: <% c.profile.registration.phone |h %>
</p>

<hr />

<p>
shell:
%		if c.profile.registration.shelltext:
<% c.profile.registration.shelltext |h %>
%		else:
<% c.profile.registration.shell |h %>
%		#endif
</p>

<p>
editor:
%		if c.profile.registration.editortext:
<% c.profile.registration.editortext |h %>
%		else:
<% c.profile.registration.editor |h %>
%		#endif
</p>

<p>
distro:
%		if c.profile.registration.distrotext:
<% c.profile.registration.distrotext |h %>
%		else:
<% c.profile.registration.distro |h %>
%		#endif
</p>

<p>
description: <% c.profile.registration.silly_description |h %>
</p>

<p>
teesize: <% c.profile.registration.teesize |h %>
</p>

<p>
Additional dinner tickets: <% c.profile.registration.dinner |h %>
</p>

<p>
Dietary requirements: <% c.profile.registration.diet |h %>
</p>

<p>
Special requirements: <% c.profile.registration.special |h %>
</p>

<p>
Number of people you've invited to Open Day: <% c.profile.registration.opendaydrag |h %>
</p>

<hr />

<p>
Partner's email address: <% c.profile.registration.partner_email |h %>
</p>

<p>
Kids coming: aged 0-3: <% c.profile.registration.kids_0_3 |h %>; 4-6: <% c.profile.registration.kids_4_6 |h %>; 7-9: <% c.profile.registration.kids_7_9 |h %>; 10+: <% c.profile.registration.kids_10 |h %>
</p>

<hr />

<p>
Accommodation: <% c.profile.registration.accommodation.name |h %> <% c.profile.registration.accommodation.option |h %>
</p>

<p>
check-in date: <% c.profile.registration.checkin |h %> January 2007
</p>

<p>
check-out date: <% c.profile.registration.checkout |h %> January 2007
</p>

<hr />

<p>
join Linux Australia: <% c.profile.registration.lasignup |h %>
</p>

<p>
Join the conference announcement list: <% c.profile.registration.announcesignup |h %>
</p>

<p>
Join the delegates discussion list: <% c.profile.registration.delegatesignup |h %>
</p>

<hr />

<p>
Previous miniconfs: <% c.profile.registration.prevlca |h %>
</p>

<p>
Miniconfs likely to attend: <% c.profile.registration.miniconf |h %>
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
