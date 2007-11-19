<% c.text %>
<table>
<tr>
% for header in c.columns:
  <th><% header %></th>
% # endfor
</tr>

% rows = 0
% for row in c.data:
  <tr class="<% oddeven.next() %>">
%   rows += 1
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
(<% rows |h %> rows)<br/>

<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven()
</%init>
