    <table>
      <tr>
        <th>rego</th>
        <th>invoice</th>
        <th>created</th>
        <th>person</th>
        <th>amount</th>
        <th>status</th>
        <th>payment(s)</th>
      </tr>
% for i in c.invoice_collection:
      <tr class="<% oddeven() %>">
%   if i.person.registration:
%       r = i.person.registration
          <td><% h.link_to('id: ' + str(r.id), h.url(controller='registration', action='view', id=r.id)) %></td>
%   else:
          <td>-</td>
%   #endif
        <td><% h.link_to('id: ' + str(i.id), h.url(action='view', id=i.id)) %></td>
        <td><% i.creation_timestamp |h %></td>
        </td>
        <td><% h.link_to(m.apply_escapes(i.person.firstname + ' ' + i.person.lastname, 'h'), h.url(controller='person', action='view', id=i.person.id)) %></td>
        <td align="right"><% "$%.2f" % (i.total()/100.0) %></td>
        <td><% i.status() %></td>
        <td>
%   if i.good_payments:
%       for p in i.good_payments:
%           if p.Amount != i.total():
          <b>mismatch!</b>
%           #endif
          <% "$%.2f" % (p.Amount / 100.0) %>
          <small><% p.TransID |h%></small>
%           if p.HTTP_X_FORWARDED_FOR != '203.89.255.156':
          <br><b>unknown IP!</b>
          <% p.HTTP_X_FORWARDED_FOR |h%>
%           #endif

%       #endfor
%   else:
          -
%   #endif
        </td>
%   if i.bad_payments:
        <td>Bad payment(s)!</td>
%   #endif
      </tr>
% #endfor
    </table>

<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven().next
</%init>
