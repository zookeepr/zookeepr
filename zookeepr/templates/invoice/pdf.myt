% date_format = "<date><day>%d</day><month>%b</month><year>%Y</year></date>"
<invoice>
  <number><% c.invoice.id %></number>
  <issued><% c.invoice.issue_date.strftime(date_format) %></issued>
  <due><% c.invoice.due_date.strftime(date_format) %></due>

% amt = c.invoice.total()
  <amount cents="<% amt %>"><% h.number_to_currency(amt/100.0) %></amount>
% if c.invoice.good_payments:
  <paid>
% pp = []
%   for p in c.invoice.good_payments:
%     pp.append(p.TransID)
%   #endfor
    <transaction><% '-'.join(pp) %></transaction>
  </paid>
% elif c.invoice.total() == 0:
  <zero/>
% else:
  <owed/>
% #endif
% if c.invoice.bad_payments:
  <badpayments/>
% #endif

  <name><% c.invoice.person.firstname %> <% c.invoice.person.lastname %></name>
  <firstname><% c.invoice.person.firstname %></firstname>
  <lastname><% c.invoice.person.lastname %></lastname>
  <email><% c.invoice.person.email_address %></email>

% if c.invoice.person.registration and c.invoice.person.registration.company:
%   rego = c.invoice.person.registration
  <company><% rego.company %></company>
  <address>
    <address1><% rego.address1 %></address1>
    <address2><% rego.address2 %></address2>
    <city><% rego.city %></city>
    <country><% rego.country %></country>
    <postcode><% rego.postcode %></postcode>
  </address>
% # endif

  <event><% h.event_name() %></event>

  <items>
% for item in c.invoice.items:
    <item>
      <description><% item.description %></description>
      <qty><% item.qty %></qty>
      <each cents="<% item.cost %>"><% h.number_to_currency(item.cost/100.0) %></each>
      <subtotal><% h.number_to_currency(item.total()/100.0) %></subtotal>
    </item>
% #endfor
  </items>

% gst = c.invoice.total()/11.0
  <gst cents="<% '%.2f'%gst %>"><% h.number_to_currency(gst/100.0) %></gst>

</invoice>
