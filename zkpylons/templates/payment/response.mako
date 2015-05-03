To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
%if not c.response['approved']:
Subject: Rejected payment attempt for ${ c.config.get('event_name') }

Your payment was unsuccessful. The reason was:

    ${ c.pr.response_text }

You can try again by visiting:
  ${ h.url_for(qualified=True, controller='registration', id=c.pr.invoice.person.registration.id, action='pay') }
%else:
Subject: Successful payment for ${ c.config.get('event_name') }

Your payment for ${ h.integer_to_currency(c.response['amount_paid']) } was successful.

Your receipt number is: PR${ c.pr.id }P${ c.pr.payment.id }

%  if c.pr.invoice:
You can view your invoice at
  ${ h.url_for(qualified=True, controller='invoice', id=c.pr.invoice.id, action='view') }

%  endif
Thanks again, and have a great day!
%endif

The ${ c.config.get('event_name') } Organising Committee
