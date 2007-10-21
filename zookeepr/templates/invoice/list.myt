<table>
<th>invoice</th>
<th>person</th>
<th>amount</th>
<th>status</th>
<th>payment(s)</th>
% for i in c.invoice_collection:
  <tr class="<% oddeven() %>">
    <td><a href="/invoice/<% i.id %>"><% i.id %></a></td>
    <td><a href="/profile/<% i.person.id %>"><% i.person.firstname |h%> <%
    i.person.lastname |h%></a></td>
    <td align="right"><% "$%.2f" % (i.total()/100.0) %></td>
    <td>
%  if i.paid():
      <b>paid</b>
%  else:
      &nbsp;
%  #endif
    </td>
    <td>
%  if i.good_payments:
%    for p in i.good_payments:
%      if p.Amount != i.total():
       <b>mismatch!</b>
%      #endif
       <% "$%.2f" % (p.Amount / 100.0) %>
       <small><% p.TransID |h%> /
       <% p.HTTP_X_FORWARDED_FOR |h%></small>

%    #endfor
%  else:
-
%  #endif
    </td>
%  if i.bad_payments:
    <td>
     Bad payment(s)!
    </td>
%  #endif
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

