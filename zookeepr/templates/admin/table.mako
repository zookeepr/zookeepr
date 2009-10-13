<%inherit file="/base.mako" />
<%
    rows = 0
%>

<p> ${ c.text | n } </p>
<table>
<tr>
% for header in c.columns:
  <th>${ header }</th>
%  endfor
</tr>

% for row in c.data:
<%   rows = rows + 1 %>
  <tr class="${ h.cycle('even', 'odd') }">
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
<p>(${ rows |h } rows)</p>
<p>${ h.link_to("Back to admin list", h.url_for(controller='admin')) }</p>



