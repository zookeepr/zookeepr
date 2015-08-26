<%inherit file="/base.mako" />

<h1>Pay invoice</h1>

<strong>Invoice #:</strong>
${ c.payment.invoice.id }
</p>

<p>
<strong>Amount:</strong>
${ h.integer_to_currency(c.payment.amount) }
</p>

${ h.form('https://vault.safepay.com.au/cgi-bin/test_payment.pl') }
${ h.hidden('payment_reference', c.config.get('event_shortname') + ' i-' + str(c.payment.invoice.id) + ' p-' + str(c.payment.id)) }
${ h.hidden('vendor_name', 'linux') }
${ h.hidden('cards_accepted', 'VISA,MASTERCARD,AMEX') }
${ h.hidden('gst_rate', '10') }
${ h.hidden('gst_added', 'TRUE') }
${ h.hidden(c.config.get('event_name') + ' Registration', h.integer_to_currency(c.payment.amount, unit='') }
${ h.hidden('hidden_fields', 'submit') }
${ h.hidden('receipt_address', c.payment.invoice.person.email_address) }
${ h.hidden('return_link_text', 'Return to ' + c.config.get('event_name')) }
${ h.hidden('return_link_url', h.url_for(qualified=True, controller='invoice', action='view', id=c.payment.invoice.id)) }
${ h.hidden('reply_link_url', h.url_for(protocol='http', qualified=True, controller='payment', action='new', id=c.payment.id) + '?payment_id=' + str(c.payment.id) + '&invoice_id=' + str(c.payment.invoice.id) + '&summary_code=&response_amount=&currency=&card_name=&card_type=&card_number=&card_expiry=&card_mac=&response_code=&bank_reference=&response_text=&remote_ip=&receipt_address=') }

<p>${ h.submit('submit', 'Pay through SecurePay') }

<p>Payment gateway kindly provided by:<br/>
<img src="/images/securepay.jpg"></p>

<p>
View ${ h.link_to('invoice details', url=h.url_for(action='view')) } or ${
h.link_to('registration status', url=h.url_for(controller='registration', action='status')) } before
payment.
</p>
