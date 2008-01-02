<% c.message %>
<% h.form(h.url()) %>
% for a in areas:
<p class="entries"><% a %> <% h.check_box(a, checked = a in selected) %></p>
%   if desc.has_key(a):
<p class="note"><% desc[a] %></p>
%   #endif
% #endfor

<p class="entries">Other: <% h.text_field('other', size=100, value=other) %>
<p class="note">Any other areas of interest or useful skills.</p>

<p class="submit"><% h.submit('Update') %></p>

<% h.end_form() %>

<%init>
areas = (
'A/V',
'week before', 'week after'
)
desc = {
  'week before': 'Available during the week before the conference (21-26 Jan)',
  'week after': 'Available during the week after the conference (3-8 Feb)',
}
selected = []; other = []
for a in c.registration.volunteer.split(';'):
  a = a.strip();
  if a in areas:
      selected.append(a)
  else:
      other.append(a)
other = '; '.join(other)
</%init>
