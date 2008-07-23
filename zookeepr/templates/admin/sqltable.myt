<p><% h.link_to('Export as CSV', url=h.url(controller='admin', action='csv')) %></p>

<table border="1">
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
      <td class="list">
%     try:
        <% item | h %>
%     except:
        <% `item` | h %>
%     #endtry
      </td>
%   # endfor
  </tr>
% # endfor
</table>
<p>(<% rows |h%> rows)</p>

% if h.debug():
    <br><p class="note">
    <% c.sql %>
    </p>
% # endif

<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven()
</%init>
