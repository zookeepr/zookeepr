<& actions &>

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
<strong>Amount Due:</strong> $0.00
</p>
% else:
<p>
<strong>Amount Due:</strong> <% h.number_to_currency(c.invoice.total()/100) %>
</p>
% #endif

<p>
<strong>Attention:</strong> <% c.invoice.person.fullname %>
</p>

<p>
<strong>Regarding:</strong> linux.conf.au 2007
</p>

<p>
This invoice has been issued as a result of an application to attend
linux.conf.au 2007, being held at the University of New South Wales
in Sydney, Australia.
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
Further information on your registration is available at
<a href="/profile">http://lca2007.linux.org.au/profile</a>.
</p>

<p>
Enquiries may be emailed to the organisers:
<a href="mailto:seven-contact@lca2007.linux.org.au">seven-contact@lca2007.linux.org.au</a> .
</p>

<div style="text-align:center">
<p>
<a href="http://linux.conf.au">linux.conf.au</a> is a project of <a href="http://linux.org.au">Linux Australia, Incorporated</a>.
</p>
<p>
              GPO Box 4788,  Sydney NSW 2001, Australia
<br />
                         ABN 56 987 117 479
#                         NZ GST #90-792-369
<br />
                        fax: +61 2 8211 5211
</p>
</div>

#</pre>

<& actions &>

<%method actions>
% if c.invoice.bad_payments:
Invalid payments have been applied to this invoice, please email <a href="mailto:seven-contact@lca2007.linux.org.au">seven-contact@lca2007.linux.org.au</a>
% elif not c.invoice.good_payments:
<p>
#<% h.link_to('Pay this invoice', url=h.url(controller='invoice', action='pay')) %>
</p>
% else:
Invoice has been paid.
% #endif
</%method>

<%method title>
Tax Invoice/Statement - <& PARENT:title &>
</%method>
