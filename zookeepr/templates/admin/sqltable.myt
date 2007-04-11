<table>
<tr>
% for header in c.columns:
  <th><% header %></th>
% # endfor
</tr>

% for row in c.data:
  <tr>
%   for item in row:
    <td><% item | h%></td>
%   # endfor
  </tr>
% # endfor
</table>

<pre>
<% c.sql %>
</pre>
