<h1>Professional attendees</h1>

<h2>Fairy Penguin Sponsors</h2>

<table>
#<tr>
#% for header in c.columns:
#  <th><% header %></th>
#% # endfor
#</tr>

% oe = oddeven()
% for (p, r) in c.fairies:
  <tr class="<% oe.next() %>">
    <td><% p.firstname |h%> <% p.lastname |h%></td>
    <td><% r.company |h%></td>
  </tr>
% # endfor
</table>

<h2>Professional</h2>

<table>
#<tr>
#% for header in c.columns:
#  <th><% header %></th>
#% # endfor
#</tr>

% oe = oddeven()
% for (p, r) in c.profs:
  <tr class="<% oe.next() %>"
%   if r.type=='Fairy Penguin Sponsor':
      style="font-weight: bold"
%   #endif
  >
    <td><% p.firstname |h%> <% p.lastname |h%></td>
    <td><% r.company |h%></td>
  </tr>
% # endfor
</table>

<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
</%init>
