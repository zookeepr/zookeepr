<h1>Pay invoice</h1>

<form method="POST"
  action="https://vault.safepay.com.au/cgi-bin/test_payment.pl"
  onSubmit="return disableForm(this);" >

# % for k in fields.keys():
# <input type="hidden" name="<% k %>" value="<% fields[k] %>">
# % # end for

<input type="hidden" name="Invoice <% fields['InvoiceID'] %>"
  VALUE="<% "%.2f" % (fields['Amount']/100.0) %>">

<p>
<strong>Invoice #:</strong>
<% fields['InvoiceID'] %>
</p>

<p>
<strong>Amount:</strong>
<% h.number_to_currency(fields['Amount']/100.0) %>
</p>

<p>
<% h.link_to('Go back', url=h.url(action='view')) %> to view invoice details,
or <% h.link_to('view registration details', url='/profile') %> before payment.
</p>

<input type="hidden" name="receipt_address"
  value="<% c.invoice.person.email_address |h %>">

<INPUT TYPE="HIDDEN" NAME="vendor_name" VALUE="linux">

<input type="submit" value="Go to the SecurePay checkout">
</form>

<%args>
fields
</%args>
