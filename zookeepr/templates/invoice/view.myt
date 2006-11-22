<h1>Tax Invoice/Statement</h1>

<div style="text-align:center">
<p>
                         Linux Australia Incorporated
</p>
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
<th>Total</th>
</tr>

% for item in c.invoice.items:
<tr>

<td>
<% item.description %>
</td>

<td style="text-align:center">
<% item.qty %>
</td>

<td>
<% item.cost %>
</td>

<td>
<% item.total() %>
</td>

</tr>
% #endif
<tr></tr>
<tr>
<td style="text-align: right" colspan="3">Total</td>
<td><% c.invoice.total() %></td>
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

# if invoice unpayed
<p><a href="asdf">Confirm Invoice</a></p>
# endif
