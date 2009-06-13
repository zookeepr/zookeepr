<% date_format = "<date><day>%d</day><month>%b</month><year>%Y</year></date>" %>
<invoice>
  <logo>/home/josh/LCA09/website/registrations/zookeepr/templates/invoice/tuz.png</logo>
  <number>${ c.invoice.id }</number>
  <issued>${ c.invoice.issue_date.strftime(date_format) }</issued>
  <due>${ c.invoice.due_date.strftime(date_format) }</due>

<% amt = c.invoice.total() %>
  <amount cents="${ amt }">${ h.number_to_currency(amt/100.0) }</amount>
% if c.invoice.good_payments:
  <paid>
<% pp = [] %>
%   for p in c.invoice.good_payments:
<%     pp.append(str(p.TransID)) %>
%   endfor
    <transaction>${ '-'.join(pp) }</transaction>
  </paid>
% elif c.invoice.total() == 0:
  <zero/>
% else:
  <owed cents="${ amt }"/>
% endif
% if c.invoice.bad_payments:
  <badpayments/>
% endif

  <name>${ c.invoice.person.firstname | h } ${ c.invoice.person.lastname | h }</name>
  <firstname>${ c.invoice.person.firstname | h }</firstname>
  <lastname>${ c.invoice.person.lastname | h }</lastname>
  <email>${ c.invoice.person.email_address | h }</email>

  <company>${ c.invoice.person.company | h }</company>
  <address>
    <address1>${ c.invoice.person.address1 | h }</address1>
    <address2>${ c.invoice.person.address2 | h }</address2>
    <city>${ c.invoice.person.city | h }</city>
    <country>${ c.invoice.person.country | h }</country>
    <postcode>${ c.invoice.person.postcode | h }</postcode>
    <state>${ c.invoice.person.state | h }</state>
  </address>

  <event>${ h.event_name() }</event>
  <contact>${ h.lca_info['contact_email'] }</contact>

  <itemcount>${ len(c.invoice.items) }</itemcount>
  <items>
<% itemid = 0 %>
% for item in c.invoice.items:
<%   itemid += 1 %>
    <item${ itemid }>
      <description>${ item.description }</description>
      <qty>${ item.qty }</qty>
      <each cents="${ item.cost }">${ h.number_to_currency(item.cost/100.0) }</each>
      <subtotal cents="${ item.total() }">${ h.number_to_currency(item.total()/100.0) }</subtotal>
    </item${ itemid }>
% endfor
  </items>

<% gst = int(c.invoice.total()/11.0 + 0.5) %>
# +0.5 for rounding
  <gst cents="${ gst }">${ h.number_to_currency(gst/100.0) }</gst>

</invoice>
