<%python>
status = []
if c.invoice.good_payments:
  status.append('paid')
  if len(c.invoice.good_payments)>1:
    status[-1] += ' (%d times)' % len(c.invoice.good_payments)
if c.invoice.bad_payments:
  status.append('tried to pay')
  if len(c.invoice.bad_payments)>1:
    status[-1] += ' (%d times)' % len(c.invoice.bad_payments)
status = ' and '.join(status)
</%python>

<h2>Invoice already <% status %></h2>

<p>The invoice is marked as <% status %>. Please go to the <a
href="/registration/status">registration status page</a> or
<% h.contact_email('contact the committee') %> to clear up the
situation.</p>

