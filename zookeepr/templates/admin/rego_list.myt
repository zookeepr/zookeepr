<table>
<tr>
  <th>Name</th>
  <th>Rego</th>
  <th>Invoices</th>
  <th>T-shirt</th>
  <th>Accom</th>
  <th>Remarks</th>
</tr>
% for registration in c.data:
%   person = registration.person
%   invoices = person.invoices
%   comments = []
<tr class=<% oddeven() %>">
<td><% person.firstname |h%> <% person.lastname |h%>
&lt;<a href="mailto:<% person.email_address |h%>"><% person.email_address |h%></a>&gt;
<br><% registration.company |h%></td>
<td>
%   if person.is_speaker():
%     comments.append('speaker')
%   #endif
%   if person.roles:
%     comments.append('roles: ' + ', '.join([role.name for role in person.roles]))
%   #endif
<b><% registration.type |h%></b> <a href="/registration/<%registration.id%>"><%registration.id%></a>
</td><td>
%   if invoices:
%     for i in invoices:
<a href="/invoice/<%i.id%>"><% i.id %></a> (<% h.number_to_currency(i.total()/100.0) %><% yesno(i.paid(), '', ' <b>not paid</b>')%>)
%     #endfor
%   #endif
</td><td>
<% registration.teesize |h%>
%   if registration.extra_tee_count:
 + <%  registration.extra_tee_count |h%>: <% registration.extra_tee_sizes %>
%   #endif

%   if not registration.prevlca:
%     comments.append('first-time')
%   #endif

%   if registration.dinner:
%     comments.append('+%d dinners'% registration.dinner)
%   #endif

%   if registration.diet:
%     comments.append('diet: %s' % registration.diet)
%   #endif
%   if registration.special:
%     comments.append('special: %s' % registration.special)
%   #endif
</td>
<td>
%   if registration.accommodation:
<% registration.accommodation.name %>
%       if registration.accommodation.option:
(<% registration.accommodation.option %>)
%       #endif
# - $<% "%.2f" % registration.accommodation.cost_per_night %> per night;
<% registration.checkin %>&#8211;<% registration.checkout %>
%   else:
-
%   #endif
</p>

<td>
<% '; '.join(comments) |h%>
</td>

</tr>
% #endfor
</table>

<%init>
def yesno(cond, yes, no):
  if cond:
    return yes
  else:
    return no

def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven().next

</%init>
