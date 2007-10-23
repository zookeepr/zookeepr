<% c.text %>
<table>
<tr>
% for header in c.columns:
  <th><% header %></th>
% # endfor
</tr>

% for row in c.data:
  <tr class="<% oddeven.next() %>">
%   for item in row:
%     if c.noescape:
        <td class="list"><% item %></td>
%     else:
        <td class="list"><% item |h%></td>
%     #endif
%   # endfor
  </tr>
% # endfor
</table>

<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven()
</%init>
