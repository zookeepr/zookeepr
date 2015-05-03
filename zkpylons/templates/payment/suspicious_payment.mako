To: ${ c.config.get('contact_email') }
Subject: Suspicious payment from ${ c.person.firstname } ${ c.person.lastname }

Payment:         ${ c.pr.payment.id }
%if c.pr.invoice is not None:
Invoice:         ${ c.pr.invoice.id }
%else:
Invoice:         INVALID
%endif
PaymentReceived: ${ c.pr.id }

${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
submitted a payment which was approved but the following validation errors
occurred:

    ${ '\n    '.join(c.pr.validation_errors.split(';')) }

More details can be seen here:
  ${ h.url_for(qualified=True, controller='payment', action='view', id=c.pr.payment.id) }
