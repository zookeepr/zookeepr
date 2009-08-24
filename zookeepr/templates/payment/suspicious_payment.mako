To: ${ h.lca_info['contact_email'] }
Subject: Suspicious payment from ${ c.person.firstname } ${ c.person.lastname }

Payment:         ${ c.pr.payment.id }
Invoice:         ${ c.pr.invoice.id }
PaymentReceived: ${ c.pr.id }

${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
submitted a payment which was approved but the following validation errors
occurred:

    ${ c.pr.validation_errors }

More details can be seen here:
  ${ h.lca_info['event_url'] }/payment/${ c.pr.payment.id }
