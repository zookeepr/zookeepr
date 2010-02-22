<%inherit file="/base.mako" />

<h1>Pay invoice</h1>

<strong>Invoice #:</strong>
${ c.payment.invoice.id }
</p>

<p>
<strong>Amount:</strong>
${ h.number_to_currency(c.payment.amount/100.0) }
</p>

${ h.form(h.url_for()) }
${ h.hidden('payment_id', c.payment.id) }
<p>${ h.submit('submit', 'Pay through Payment Express') }

<p>
View ${ h.link_to('invoice details', url=h.url_for(action='view')) } or ${
h.link_to('registration status', url=h.url_for(controller='registration', action='status')) } before
payment.
</p>

<p><img alt="[DPS logo]" style="margin-right: 0.5em" src="/images/paymentexpress.png"/>
Hosted payment solution kindly provided by Payment Express</p>
