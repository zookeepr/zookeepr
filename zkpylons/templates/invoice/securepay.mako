<%inherit file="/base.mako" />

<h1>Pay invoice</h1>

<strong>Invoice #:</strong>
${ c.payment.invoice.id }
</p>

<p>
<strong>Amount:</strong>
${ h.integer_to_currency(c.payment.amount) }
</p>

${ h.form(c.payment.gateway_url) }
${ h.hidden('bill_name', 'transact') }
${ h.hidden('merchant_id', c.payment.merchant_id) }
${ h.hidden('txn_type', c.payment.transaction_type) }
${ h.hidden('primary_ref', c.payment.transaction_reference) }
${ h.hidden('amount', c.payment.amount) }
${ h.hidden('fp_timestamp', c.payment.creation_timestamp_utc_formattedstring) }
${ h.hidden('fingerprint', c.payment.securepay_fingerprint) }
${ h.hidden('display_cardholder_name', 'yes') }
${ h.hidden('email_address', c.payment.invoice.person.email_address) }
${ h.hidden('return_url', h.url_for(qualified=True, controller='invoice', action='view', id=c.payment.invoice.id)) }
${ h.hidden('return_url_text', 'Return to ' + c.payment.event_name) }
${ h.hidden('callback_url', h.url_for(protocol='http', qualified=True, controller='payment', action='new')) }
<input type="hidden" name="card_types" value="VISA|MASTERCARD|AMEX">
${ h.hidden('page_header_image', h.url_for('/img/Geelong-Wave-Gradient-medium.png', protocol='http')) }
${ h.hidden('page_style_url', h.url_for('/css/invoice.css', protocol='http')) }
<p>${ h.submit('', 'Pay through SecurePay') }

<p>Payment gateway kindly provided by:<br/>
<img src="/img/securepay.jpg"></p>

<p>
View ${ h.link_to('invoice details', url=h.url_for(action='view')) } or ${
h.link_to('registration status', url=h.url_for(controller='registration', action='status')) } before
payment.
</p>
