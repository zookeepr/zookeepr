<h1>Volunteer preferences, skills and abilities</h1>
<% c.message %>
% if c.signed_in_person.id != c.registration.person.id:
<p><b>You're looking at (and editing) <% c.registration.person.firstname |h%>
<% c.registration.person.lastname |h%>'s info, not your own!</b></p>
% #endif
<% h.form(h.url()) %>
<table>
% for a in areas:
<tr class="<% oddeven() %>"><td><% a %>
%   if desc.has_key(a):
<p class="note"><% desc[a] %></p>
%   #endif
<td><p class="entries">
<% h.check_box(a, checked = a in selected) %></p>
% #endfor
</table>

<p class="entries">Other: <% h.text_field('other', size=80, value=other) %>
<p class="note">Any other areas of interest or useful skills.</p>

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
'Venue Helper',

'driver',

'week before', 'week after',
)
desc = {
  'Network helper': 'short term',
  'Partners Program helper': 'short term',
  'Venue Helper': 'helping with setting up break times, managing venues and introducing speakers, etc',
  'driver': "Have driver's licence, will travel.",
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
