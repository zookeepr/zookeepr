To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
%if not c.response['approved']:
Subject: Rejected payment attempt for ${ h.lca_info['event_name'] }

Your payment was unsuccessful. The reason was:

    ${ c.pr.response_text }

You can try again by visiting:
  ${ h.lca_info['event_url'] }/registration/${ c.pr.invoice.person.registration.id }/pay
%else:
Subject: Sucessful payment for ${ h.lca_info['event_name'] }

Your payment for ${ h.number_to_currency(c.response['amount_paid'] / 100.0) } was successful.

Your receipt number is: PR${ c.pr.id }P${ c.pr.payment.id }

%  if c.pr.invoice:
You can view your invoice at
  ${ h.lca_info['event_url'] }/invoice/${ c.pr.invoice.id }

%  endif
Thanks again, and have a great day!
%endif

The ${ h.lca_info['event_name'] } Organising Committee
