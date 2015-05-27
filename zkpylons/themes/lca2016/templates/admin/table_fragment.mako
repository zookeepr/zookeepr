<%
    rows = 0
%>

<p> ${ c.text | n } </p>
<table class="table table-bordered">
<tr>
% for header in c.columns:
  <th>${ header }</th>
%  endfor
</tr>

% for row in c.data:
  <tr class="${ rows % 2 == 0 and "odd" or "even" }">
    <% rows += 1 %>
%   for item in row:
%     if c.noescape:
        <td class="list">${ item | n}</td>
%     else:
        <td class="list">${ item | h}</td>
%     endif
%    endfor
  </tr>
% endfor
</table>
<br>


