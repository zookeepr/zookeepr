<h1>Volunteer preferences, skills and abilities</h1>
<% c.message %>
% if c.signed_in_person.id != c.registration.person.id:
<p><b>You're looking at (and editing) <% c.registration.person.firstname |h%>
<% c.registration.person.lastname |h%>'s info, not your own!</b></p>
% #endif
<% h.form(h.url()) %>
<table>
% for a in areas:
<tr class="<% oddeven() %>">
<td valign="middle" align="center"><% h.check_box(a, checked = a in selected) %></td>
<td><% a %>
%   if desc.has_key(a):
<br><small><% desc[a] %></small>
%   #endif
</td>
</tr>
% #endfor
<tr class="<% oddeven() %>">
<td colspan="2">
<p class="entries">Other: <% h.text_field('other', size=80, value=other) %></p>
<p class="note">Any other areas of interest or useful skills. Arrival and
departure dates, if you're not local.</p>
</td></tr>
<tr class="<% oddeven() %>">
<td colspan="2">
<p class="entries">Phone: <% h.text_field('phone', size=40, value=c.registration.phone or c.registration.person.phone) %></p>
<p class="note">Your phone number, preferrably a mobile (cell) phone you'll
have with you during the conference.</p>
</td></tr>
</table>

<p class="submit"><% h.submit('Update') %></p>

<% h.end_form() %>

<%init>
areas = (
'Administration', 'Rego Desk',
'AV',
'Network helper',
'Partners Program helper',
'Exec Offsider', 'Runner',
'Speaker Liaison helper',
'Venue Helper', 'Usher',

'driver', 'car',

'week before', 'week after',
)
desc = {
  'Network helper': 'short term',
  'Partners Program helper': 'short term',
  'Venue Helper': 'helping with setting up break times, managing venues and introducing speakers, etc',
  'driver': "Have driver's licence, will travel.",
  'car': "Have car, will travel.",
  'week before': 'Available during the week before the conference (21-26 Jan)',
  'week after': 'Available during the week after the conference (3-8 Feb)',
}
selected = []; other = []
for a in (c.registration.volunteer or '').split(';'):
  a = a.strip();
  if a in areas:
      selected.append(a)
  else:
      other.append(a)
other = '; '.join(other)

def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven().next
</%init>
