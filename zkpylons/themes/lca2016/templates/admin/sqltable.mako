<%inherit file="/base.mako" />
<%
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven()
%>

<h1>${ h.url_for().split('/')[-1].replace('_', ' ').title() }</h1>
<p><a href="?csv=true">Export as CSV</a></p>

<table class="table sortable">
<tr>
% for header in c.columns:
  <th>${ header }</th>
% endfor
</tr>

<% rows = 0 %>
%for row in c.data:
  <tr class="${ oddeven.next() }">
<%   rows += 1 %>
%   for item in row:
      <td class="list">
        ${ item | h }
      </td>
%   endfor
  </tr>
%endfor
</table>
<p>(${ rows |h} rows)</p>

<br>
<p>${ h.link_to("Back to admin list", h.url_for(controller='admin')) }</p>

% if h.debug():
    <br><p class="note">
    ${ c.sql }
    </p>
% endif
