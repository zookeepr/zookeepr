<% h.form(h.url(), method='get') %>
<p class="entries" style="float: right">ID or name: <% h.textfield('id', size=10, tabindex=1) %></p>
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
  <tr class="<% oddeven1() %>">
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
&lt;<a href="mailto:<% person.email_address |h%>"><% person.email_address |h%></a>&gt; (<a href="/profile/<% person.id |h%>"><% person.id |h%></a>)
<br><% registration.company |h%></p>

<p>
%   if person.is_speaker():
<strong>speaker</strong><br>
%   #endif
%   if person.roles:
<strong><% ', '.join([role.name for role in person.roles]) %></strong><br>
%   #endif
%   if registration:
<% h.form(h.url(), method='post') %>
<p class="entries" style="float: right">Add note:
<% h.textfield('note', size=30, tabindex=2, value='Here!') %>
<% h.hidden_field('id', value=registration.id) %>
</p>
<% h.end_form() %>
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

%   if registration.phone or person.phone:
<p>Phone: <% registration.phone or person.phone |h%></p>
%   #endif

%   PP = []
%   for k in ('pp_adults', 'kids_0_3', 'kids_4_6', 'kids_7_9', 'kids_10_11', 'kids_12_17'):
%     count = getattr(registration, k, 0)
%     if count:
%       PP.append('%d&#215; %s' % (count, k.replace('_', ' ',1).replace('_', '-')))
%     #endif
%   #endfor
%   if PP:
<p>PP: <% ", ".join(PP) %></p>
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

%     if registration.type in ("Monday pass", "Tuesday pass", "Monday only", "Tuesday only"):
No included dinner.
%     #endif

%     if registration.dinner:
<% registration.dinner %> additional dinner tickets.
%     #endif

%     if registration.voucher:
Voucher:
<% registration.voucher.percentage %>% <% registration.voucher.type %>
&#8212;
<% registration.voucher.code.split('-')[0] %>
&#8212;
<% registration.voucher.comment |h%>
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
  <tr class="<% oddeven1() %>">
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

% if registration and registration.notes:
<table width="100%">
  <tr>
    <th>when</td>
    <th>note</td>
    <th>by</td>
  </tr>
%   for n in registration.notes:
  <tr class="<% oddeven2() %>">
    <td align="left"><% n.entered.strftime('%Y-%m-%d %a %H:%M:%S') %></td>
    <td align="left"><% n.note |h%></td>
    <td align="left"><% n.by.firstname |h%> <% n.by.lastname |h%></td>
  </tr>
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
oddeven1 = oddeven().next
oddeven2 = oddeven().next

class blank:
  def __getattr__(self, name):
    return false_dash()
  def __nonzero__(self):
     return 0

class false_dash:
  def __nonzero__(self):
     return 0
  def __str__(self):
    return '-'

registration = c.r
person = c.p
invoices = c.i

if not registration:
  registration = blank()
</%init>
