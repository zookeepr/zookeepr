<% h.form(h.url()) %>
<p class="entries" style="float: right">ID: <% h.text_field('id', size=10, tabindex=1) %></p>
<% h.end_form() %>
% if c.error:
%   if c.id:
Error looking up <% c.id |h%>:
%   #endif
<% c.error %>
% else:
<p>Looked up: <% c.id |h%></p>

<p><b><% person.firstname |h%> <% person.lastname |h%></b>
&lt;<a href="mailto:<% person.email_address |h%>"><% person.email_address |h%></a>&gt;
<br><% registration.company |h%></p>

<p>
%   if person.is_speaker():
<strong>speaker</strong><br/>
%   #endif
%   if person.roles:
<strong><% ', '.join([role.name for role in person.roles]) %></strong><br/>
%   #endif
%   if registration:
<b><% registration.type |h%></b> rego <a href="/registration/<%registration.id%>"><%registration.id%></a>
%   else:
not registered
%   #endif
</p>

<p>
<strong><% yesno( invoices and invoices[0].paid(), 'paid', 'not paid') %></strong>
%   if invoices:
%     for i in invoices:
invoice <a href="/invoice/<%i.id%>"><% i.id %></a> (<% h.number_to_currency(i.total()/100.0) %> <% yesno(i.paid(), 'paid', 'not paid')%>)
%     #endfor
%   #endif
</p>

%   if registration:
<p>T-shirt: <% registration.teesize |h%>
%     if registration.extra_tee_count:
plus <%  registration.extra_tee_count |h%> extra: <% registration.extra_tee_sizes %>
%     #endif
</p>

<% yesno(registration.prevlca, '', '<p>first-time attendee</p>') %>

%     if registration.dinner:
<% registration.dinner %> additional dinner tickets.
%     #endif

%     if registration.diet:
<p>Dietary requirements: <% registration.diet %></p>
%    #endif
%     if registration.special:
<p>Special requirements: <% registration.special %></p>
%     #endif

<p>
Accommodation:
%     if registration.accommodation:
<% registration.accommodation.name %>
%       if registration.accommodation.option:
(<% registration.accommodation.option %>)
%       #endif
- $<% "%.2f" % registration.accommodation.cost_per_night %> per night;
check in:
<% date(registration.checkin) %>,
check out:
<% date(registration.checkout) %>.
%     else:
I will organise my own.
%     #endif
</p>
%   #endif
% #endif

% if invoices:
<table width="100%">
  <tr>
    <th>Invoice</td>
    <th>Description</td>
    <th>Qty</td>
    <th>Cost</td>
    <th>Total</td>
  </tr>
%   for i in invoices:
%     for ii in i.items:
  <tr class="<% oddeven() %>">
    <td align="center"><% i.id %><% yesno(i.paid(), '', ' (unpaid)')%></td>
    <td><% ii.description %></td>
    <td align="center"><% ii.qty %></td>
    <td align="right"><% h.number_to_currency(ii.cost/100.0) %></td>
    <td align="right"><% h.number_to_currency(ii.total()/100.0) %></td>
  </tr>
%     #endfor
%   #endfor
</table>
% #endif

<%init>
def yesno(cond, yes, no):
  if cond:
    return yes
  else:
    return no

def date(d):
    if d==1:
        return "%dst of February" % d
    elif d==2:
        return "%dnd of February" % d
    elif d==3:
        return "%drd of February" % d
    elif d<15:
        return "%dth of February" % d
    elif d==31:
        return "%dst of January" % d
    else:
        return "%dth of January" % d

def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven().next

class blank:
  def __getattr__(self, name):
    return '-'
  def __nonzero__(self):
     return 0

registration = c.r
person = c.p
invoices = c.i

if not registration:
  registration = blank()
</%init>
