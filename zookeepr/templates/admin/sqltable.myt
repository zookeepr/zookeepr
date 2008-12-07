<h1><% h.url()().split('/')[-1].replace('_', ' ').title() %></h1>
<p><a href="?csv=true">Export as CSV</a></p>

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

<br>
<p><% h.link_to("Back to admin list", h.url(controller='admin')) %></p>

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
