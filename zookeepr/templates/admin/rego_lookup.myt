<% h.form(h.url()) %>
<p class="entries" style="float: right">ID: <% h.text_field('id', size=10) %></p>
<% h.end_form() %>
% if c.error:
%   if c.id:
Error looking up <% c.id |h%>:
%   #endif
<% c.error %>
% else:
<p>Looked up: <% c.id |h%></p>
<% person.firstname |h%> <% person.lastname |h%>
&lt;<% person.email_address |h%>&gt;
<br><% registration.company |h%><br>
%   if person.is_speaker():
<strong>speaker</strong>
%   #endif
%   if registration:
<% registration.type |h%> rego <a href="/registration/<%registration.id%>"><%registration.id%></a>;
%   else:
not registered;
%   #endif
<strong><% yesno( invoices and invoices[0].paid(), 'paid', 'not paid') %></strong>
%   if invoices:
%     for i in invoices:
invoice <a href="/invoice/<%i.id%>"><% i.id %></a> (<% h.number_to_currency(i.total()/100.0) %> <% yesno(i.paid(), 'paid', 'not paid')%>)
%     #endfor
%   #endif

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
%   #endif
% #endif

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
oddeven = oddeven()

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
