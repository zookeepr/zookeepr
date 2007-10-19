<% c.xml.toprettyxml(indent="  ") %>

<hr />

<!-- 
<% c.invoice.issue_date.strftime("%d %b %Y") %>
<% c.invoice.due_date.strftime("%d %b %Y") %>
% if c.invoice.good_payments:
  Invoice Paid
% elif c.invoice.total() == 0:
  No pay required
% else:
  <% h.number_to_currency(c.invoice.total()/100.0) %>
% #endif

<% c.invoice.person.firstname %> <% c.invoice.person.lastname %>
% if c.invoice.person.registration and c.invoice.person.registration.company:
 <% c.invoice.person.registration.company %>
% # endif

<% h.event_name() %>.

% for item in c.invoice.items:
<% item.description %>
<% item.qty %>
<% h.number_to_currency(item.cost/100.0) %>
<% h.number_to_currency(item.total()/100.0) %>
% #endfor

<% h.number_to_currency(c.invoice.total()/100.0) %>
<% h.number_to_currency(c.invoice.total()/100.0/11) %>

<%method actions>
<div id="actions">
% if c.invoice.total() == 0:
%    pass
% elif c.invoice.bad_payments:
Invalid payments have been applied to this invoice, please email <% h.contact_email('the organising committee') %></a>
% elif not c.invoice.good_payments:
<p>
<% h.link_to('(Pay this invoice)', url=h.url(controller='invoice', action='pay')) %>
% if c.invoice.person.registration:
    <% h.link_to('(Regenerate invoice)', url=h.url(controller='registration', action='pay', id=c.invoice.person.registration.id)) %>
% #endif
<br>
<small>Use the regenerate invoice link to if you have edited your registration but the invoice doesn't look quite right.</small><br>
<small><strong>Please Note:</strong> To qualify for the earlybird discount you must have registred by the 15th November and you need to pay by the <strong>15th December</strong>.
</p>

% else:
Invoice has been paid.
% #endif
</div>
</%method>

<%method title>
Tax Invoice/Statement - <& PARENT:title &>
</%method>

// Convert this sucker to SVG via an XSLT transform.

// Write SVG to disk.

// Call inkscpae and convert SVG to PDF.

// Convert PDF to PS.

// Reconvert PS to PDF :-)

// Display!

// Remove temp files.

-->
