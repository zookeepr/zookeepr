To: ${ c.config.get('contact_email') }
Subject: Invoice voided by ${ c.person.firstname } ${ c.person.lastname }

Invoice:  ${ c.invoice.id }

${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }> has voided their own invoice.

This is normally done when a payment was declined and the user decided to
try again. It might be worth checking why their payment was declined though.

More details can be seen here:
  ${ h.url_for(qualified=True, controller='invoice', id=c.invoice.id) }
