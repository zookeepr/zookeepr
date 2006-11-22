<h1>Payment</h1>

<p>
% if c.payment.result != 'OK':
This is an invalid payment. Please contact seven-contact@lca2007.linux.org.au
% elif c.payment.Status == 'Accepted':
Your payment was successful. Your receipt number is <% c.payment.id %>
% else:
Your payment was unsuccessful. The reason was <% c.payment.ErrorString %>
% #endiff
</p>
