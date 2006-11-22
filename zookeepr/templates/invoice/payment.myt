<h1>Pay invoice</h1>

% print c.invoice

<form method="POST" action="https://clearance.commsecure.com.au/cgi-bin/PSCheckout">

% for k in fields.keys():
<input type="hidden" name="<% k %>" value="<% fields[k] %>">
% # end for

<p>
<strong>Invoice #:</strong>
<% fields['InvoiceID'] %>
</p>

<p>
<strong>Amount:</strong>
<% h.number_to_currency(fields['Amount']/100.0) %>
</p>

<p>
<% h.link_to('Go back', url=h.url(action='view')) %> to view invoice details, or <% h.link_to('view registration details', url='/profile') %> before payment.
</p>

<input type="submit" value="Pay via PaySecure Checkout">
</form>

<%args>
fields
</%args>
