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
% if not h.url_for().endswith('admin'):
<p>(${ rows |h } rows)</p>
<p>${ h.link_to("Back to admin list", h.url_for(controller='admin')) }</p>
% endif


