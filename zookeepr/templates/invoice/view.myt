% if c.printable:
<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>Tax Invoice/Statement - linux.conf.au 2008</title>
<link rel="icon" type="image/png" href="/favicon.png" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
</head>
<body>
% else:
<& actions &>
% #endif

<h1>Tax Invoice/Statement</h1>

<div style="text-align:center">
<h2>Linux Australia Incorporated</h2>
<p>
                             ABN 56 987 117 479
</p>
#                             NZ GST #90-792-369
</div>

<p>
<strong>Invoice Number:</strong> <% c.invoice.id %>
</p>
<p>
<strong>Issue Date:</strong> <% c.invoice.issue_date.strftime("%d %b %Y") %>
</p>
<p>
<strong>Due Date:</strong> <% c.invoice.due_date.strftime("%d %b %Y") %>
</p>
% if c.invoice.good_payments:
<p>
<strong>Invoice Paid</strong>
</p>
% elif c.invoice.total() == 0:
<p>
<strong>No Payment Required</strong>
</p>
% else:
<p>
<strong>Amount Due:</strong> <% h.number_to_currency(c.invoice.total()/100.0) %>
</p>
% #endif

<p>
<strong>Attention:</strong> <% c.invoice.person.firstname %> <% c.invoice.person.lastname %>
% if c.invoice.person.registration and c.invoice.person.registration.company:
<br />
<strong>Company:</strong> <% c.invoice.person.registration.company %>
% # endif
</p>

<p>
<strong>Regarding:</strong> <% h.event_name() %>
</p>

<p>
This invoice has been issued as a result of an application to attend
<% h.event_name() %>.
</p>

<table style="width: 100%">
<tr>
<th>Description</th>
<th>Qty</th>
<th>Cost</th>
<th>Total (Inc. GST)</th>
</tr>

% for item in c.invoice.items:
<tr class="<% h.cycle('even', 'odd') %>">

<td>
<% item.description %>
</td>

<td style="text-align:center">
<% item.qty %>
</td>

<td style="text-align:right">
<% h.number_to_currency(item.cost/100.0) %>
</td>

<td style="text-align:right">
<% h.number_to_currency(item.total()/100.0) %>
</td>

</tr>
% #endfor

<tr></tr>
<tr>

<td style="text-align: right" colspan="3">Total</td>

<td style="text-align: right">
<strong>
<% h.number_to_currency(c.invoice.total()/100.0) %>
</strong>
</td>
</tr>
<tr>

<td style="text-align: right" colspan="3">GST Included</td>

<td style="text-align: right">
<strong>
<% h.number_to_currency(c.invoice.total()/100.0/11) %>
</strong>
</td>
</tr>

</table>

<p>
Further information on your registration is available at:
<a href="/registration/status">http://<% h.host_name() %>/registration/status</a>
</p>

<p>
Enquiries may be emailed to the organisers:
% if c.printable:
<% h.contact_email() %>.
% else:
<% h.contact_email('contact email') %>.
% #endif
</p>

<div style="text-align:center">
<p>
<a href="http://linux.conf.au">linux.conf.au</a> is a project of <a href="http://linux.org.au">Linux Australia, Incorporated</a>.
</p>
<p>
              PO Box 13272, Law Courts  VIC  8010, Australia
<br />
                         ABN 56 987 117 479
#                         NZ GST #90-792-369
<br />
                        fax: +61 3 9235 5454
</p>
</div>

% if c.printable:
</body>
</html>
% else:
<& actions &>
% #endif

<%method actions>
<div id="actions">
<% h.link_to('Registration status', url=h.url(controller='registration',
action='status')) %><br/>
% if c.invoice.total() == 0:
<% h.link_to('Printable version', url=h.url(controller='invoice', action='printable')) %><br/>
% elif c.invoice.bad_payments:
Invalid payments have been applied to this invoice, please email <% h.contact_email('the organising committee') %></a>
% elif not c.invoice.paid():
<% h.link_to('Pay this invoice', url=h.url(controller='invoice', action='pay')) %><br/>
% if c.invoice.person.registration:
    <% h.link_to('Regenerate invoice', url=h.url(controller='registration', action='pay', id=c.invoice.person.registration.id)) %><br/>
% #endif
<% h.link_to('Printable version', url=h.url(controller='invoice', action='printable')) %>
<br/>
<small>Use the regenerate invoice link to if you have edited your registration but the invoice doesn't look quite right.</small><br>
<small><strong>Please Note:</strong> To qualify for the earlybird discount
you must have registered and paid by the 17th of November (unless earlybird
tickets sold out earlier).</small>
</p>

% else:
<% h.link_to('Printable version', url=h.url(controller='invoice', action='printable')) %>
<p>
Invoice has been paid.
% #endif
</div>
</%method>

<%method title>
Tax Invoice/Statement - <& PARENT:title &>
</%method>
