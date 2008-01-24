% if not c.prn:
<a href="/admin/rego_list?print">print version</a>
% #endif
<table>
<tr>
% if c.prn:
  <th>Lastname</th>
  <th>Firstname</th>
  <th>Organisation</th>
  <th>E-mail</th>
% else:
  <th>Name</th>
% #endif
  <th>Rego</th>
  <th>Invoices</th>
  <th>T-shirt</th>
% if c.prn:
  <th>Extra shirt</th>
% #endif
  <th>Accom</th>
  <th>Remarks</th>
</tr>
% for registration in c.data:
%   person = registration.person
%   invoices = person.invoices
%   comments = []
<tr class="<% oddeven() %>">
%   if c.prn:
<td valign="top"><% person.lastname |h%></td>
<td valign="top"><% person.firstname |h%></td>
<td valign="top"><% registration.company |h%></td>
<td valign="top"><% person.email_address |h%></td>
%   else:
<td valign="top"><% person.firstname |h%> <% person.lastname |h%>
&lt;<a href="mailto:<% person.email_address |h%>"><% person.email_address |h%></a>&gt;
<br><% registration.company |h%></td>
%   #endif
<td valign="top">
%   if person.is_speaker():
%     comments.append('speaker')
%   #endif
%   if person.roles:
%     comments.append('roles: ' + ', '.join([role.name for role in person.roles]))
%   #endif
<b><% registration.type |h%></b> <a href="/admin/rego_lookup?id=<%registration.id%>"><%registration.id%></a>
</td><td valign="top">
%   if invoices:
%     for i in invoices:
<a href="/invoice/<%i.id%>"><% i.id %></a> (<% h.number_to_currency(i.total()/100.0) %><% yesno(i.paid(), '', ' <b>not paid</b>')%>)
%     #endfor
%   #endif
</td><td valign="top">
<% registration.teesize |h%>
%   if c.prn:
</td><td valign="top">
%   #endif
%   if registration.extra_tee_count:
<br>+<%  registration.extra_tee_count |h%>: <% registration.extra_tee_sizes %>
%   #endif

%   if not registration.prevlca:
%     comments.append('first-time')
%   #endif

%   if registration.discount:
%     comments.append('DC: %d%% %s' % (registration.discount.percentage, registration.discount.comment))
%   #endif

%   if registration.type in ("Monday pass", "Tuesday pass", "Monday only", "Tuesday only"):
%     comments.append('no included dinner')
%   #endif

%   if registration.dinner:
%     comments.append('+%d dinners'% registration.dinner)
%   #endif

%   for k in ('pp_adults', 'kids_0_3', 'kids_4_6', 'kids_7_9', 'kids_10_11', 'kids_12_17'):
%     count = getattr(registration, k, 0)
%     if count:
%       comments.append('%d %s' % (count, k.replace('_', ' ',1).replace('_', '-')))
%     #endif
%   #endfor

%   if registration.diet:
%     comments.append('diet: %s' % registration.diet)
%   #endif
%   if registration.special:
%     comments.append('special: %s' % registration.special)
%   #endif
</td>
<td valign="top">
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

<td valign="top">
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
