% import string
<h1><% c.profile.fullname |h %></h1>

# Show personal details
% if 'signed_in_person_id' in session and session['signed_in_person_id'] == c.profile.id:

<& actions &>

<fieldset>

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

</fieldset>

%	if c.profile.registration:
<fieldset>

<p>
ticket: <% c.profile.registration.type |h %>
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


</fieldset>

<fieldset>

<p>
company: <% c.profile.registration.company |h %>
</p>

<p>
address: <% c.profile.registration.address1 |h %>
% 		if c.profile.registration.address2:
, <% c.profile.registration.address2 |h %>
%		#endif
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

</fieldset>

<fieldset>

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
Number of people you've invited to Open Day: <% c.profile.registration.opendaydrag |h %>
</p>

</fieldset>

<fieldset>

<p>
Partner's email address: <% c.profile.registration.partner_email |h %>
</p>

<p>
Kids coming: aged 0-3: <% c.profile.registration.kids_0_3 |h %>; 4-6: <% c.profile.registration.kids_4_6 |h %>; 7-9: <% c.profile.registration.kids_7_9 |h %>; 10+: <% c.profile.registration.kids_10 |h %>
</p>

</fieldset>

<fieldset>

<p>
Accommodation:
%		if c.profile.registration.accommodation:
<% c.profile.registration.accommodation.name |h %>
%			if c.profile.registration.accommodation.option:
(<% c.profile.registration.accommodation.option |h %>)
%			#endif
<% h.number_to_currency(c.profile.registration.accommodation.cost_per_night) %> per night
%		else:
none selected
%		#endif
</p>

<p>
check-in date: <% c.profile.registration.checkin |h %> January 2007
</p>

<p>
check-out date: <% c.profile.registration.checkout |h %> January 2007
</p>

</fieldset>

<fieldset>

<p>
join Linux Australia: 
% 		if c.profile.registration.lasignup:
Yes
%		else:
No
% #endif
</p>

<p>
Join the conference announcement list:
%		if c.profile.registration.announcesignup:
Yes
%		else:
No
% #endif
</p>

<p>
Join the delegates discussion list:
%		if c.profile.registration.delegatesignup:
Yes
%		else:
No
%		#endif
</p>

</fieldset>

<fieldset>

<p>
%		''' This is a HACK we should just store the years properly '''
%		if c.profile.registration.prevlca:
%			lcas = []
%			for x in c.profile.registration.prevlca:
%				if x == '99':
%					lcas.append(string.atoi('1999'))
%				else:
%					lcas.append(int(x) + 2000)
%				# endif
%			# endfor
%			lcas.sort()
 <%', '.join(['%s' % x for x in lcas]) %>
%		#endif
</p>

<p>
Miniconfs likely to attend:
%		if c.profile.registration.miniconf:
<% ', '.join(c.profile.registration.miniconf) %>
%		#endif
</p>

</fieldset>

<& actions &>

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
<% c.profile.firstname + " " + c.profile.lastname | h %> - <& PARENT:title &>
</%method>

<%method actions>
% if not c.profile.invoice or not c.profile.invoice[0].bad_payments and not c.profile.invoice[0].good_payments:
%     if c.profile.registration:
<% h.link_to('(edit registration)', url=h.url(controller='registration', action='edit', id=c.profile.registration.id)) %>
<% h.link_to('(confirm invoice and pay)', url=h.url(controller='registration', action='pay', id=c.profile.registration.id)) %>
<br>
<small><strong>Please Note:</strong> To qualify for the earlybird discount you must have registred by the 15th November and you need to pay by the <strong>8th December</strong>.
%     #endif
% else:
<% h.link_to('(View Invoice)', url=h.url(controller='invoice', action='view', id=c.profile.invoice[0].id)) %>
% #endif

</%method>

