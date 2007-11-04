<h1>Pay invoice</h1>

<form method="POST"
  action="https://vault.safepay.com.au/cgi-bin/make_payment.pl"
  onSubmit="return disableForm(this);" >

# % for k in fields.keys():
# <input type="hidden" name="<% k %>" value="<% fields[k] %>">
# % # end for

<input type="hidden" name="linux.conf.au MEL8OURNE2008"
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
View <% h.link_to('invoice details', url=h.url(action='view')) %> or <%
h.link_to('registration status', url='/registration/status') %> before
payment.
</p>

<input type="hidden" name="receipt_address"
  value="<% c.invoice.person.email_address |h %>">

<input type="hidden" name="invoice_id" value="<% fields['InvoiceID'] %>">
<input type="hidden" name="hidden_fields" value="invoice_id">
<input type="hidden" name="information_fields" value="invoice_id">

<input type="hidden" name="payment_reference"
  value="i-<% fields['InvoiceID'] %> p-<% c.invoice.person.id %>">

<INPUT TYPE="HIDDEN" NAME="vendor_name" VALUE="linux">
<input type="hidden" name="reply_link_url"
  value="http://<% h.host_name() %>/payment/new?invoice_id=&payment_amount=&bank_reference=&payment_number=">
<input type="hidden" name="return_link_url"
  value="http://<% h.host_name() %>/registration/status">
<input type="hidden" name="return_link_text"
  value="Return to the linux.conf.au website">

<p class="submit"><input type="submit" value="Go to the SecurePay checkout"></p>
</form>

<table border=0><tr><td valign="middle">
<img alt="[SecurePay logo]" width="200" height="79"
style="margin-right: 0.5em"
src="http://<% h.host_name() %>/__data/assets/image/0015/474/securepay200white.gif"
/></td>
<td valign="middle">Direct One Payment Solutions kindly provided by
SecurePay Australia</td>
</tr></table>

<%args>
fields
</%args>
