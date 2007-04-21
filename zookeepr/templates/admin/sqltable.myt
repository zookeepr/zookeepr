<table border="1">
<tr>
% for header in c.columns:
  <th><% header %></th>
% # endfor
</tr>

% for row in c.data:
  <tr class="<% oddeven.next() %>">
%   for item in row:
      <td class="list">
        <% item | h %>
      </td>
%   # endfor
  </tr>
% # endfor
</table>

<br><p class="note">
<% c.sql %>
</p>

<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven()
</%init>
