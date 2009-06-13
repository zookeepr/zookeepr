Subject: Confirmation of your payment attempt for ${ h.event_name() }
To: ${ c.person.firstname }  ${ c.person.lastname } <${ c.person.email_address }>

Thank you for your payment attempt, the results are below.

<p>
% if c.payment.result != 'OK':
This is an invalid payment. Please contact ${ h.contact_email }
% elif c.payment.Status == 'Accepted':
Your payment was successful. Your receipt number is ${ c.payment.id }
You can view your invoice at http://${ h.site_name() | u }/invoice/${ c.payment.invoice.id }
% else:
Your payment was unsuccessful. The reason was:

    ${ c.payment.ErrorString }

You can try again by visiting http://${ h.site_name() | u }/registration/${ c.payment.invoice.person.registration.id }/pay

% endif

Thanks again, and have a great day!

The ${ h.event_name() } Organising Committee
