<% h.form(h.url()) %>
<p class="entries" style="float: right">ID or name: <% h.text_field('id', size=10, tabindex=1) %></p>
<% h.end_form() %>
% if c.error:
%   if c.id:
Error looking up <% c.id |h%>:
%   #endif
<% c.error %>
% elif c.many:
<p>Looked up: <% c.id |h%> (<% c.id_type %>) but found <% len(c.many) %></p>
<table>
%   for p in c.many:
  <tr class="<% oddeven() %>">
    <td><a href="/admin/rego_lookup?id=<% p.id |h%>" tabindex="2"><% p.firstname |h%>
					       <% p.lastname |h%></td>
    <td>
%     if p.registration:
%       if p.invoices and p.invoices[0].paid():
	  <b><% p.registration.type |h%></b>
%       else:
	  not paid
%       #endif
%     else:
	no rego
%     #endif
  </tr>
%   #endfor
</table>
% else:
<p>Looked up: <% c.id |h%> (<% c.id_type %>)</p>

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
%     if invoices and invoices[0].paid():
<b><% registration.type |h%></b> rego <a href="/registration/<%registration.id%>"><%registration.id%></a>
%     else:
<b>Tentative</b> <% registration.type |h%> rego <a href="/registration/<%registration.id%>"><%registration.id%></a>; <b>not paid</b>
%     #endif
%   else:
not registered
%   #endif
</p>

%   if registration.volunteer:
<p>Volunteering areas of interest: <% registration.volunteer |h%></p>
%   #endif

<p>
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

%     if registration.discount:
Discount:
<% registration.discount.percentage %>% <% registration.discount.type %>
&#8212;
<% registration.discount.code.split('-')[0] %>
&#8212;
<% registration.discount.comment |h%>
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
