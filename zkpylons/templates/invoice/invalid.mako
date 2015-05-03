<%inherit file="/base.mako" />
<h2>Invoice invalid</h2>

<p>The invoice is marked invalid, probably because a product you have ordered is no longer available. Please
${ h.link_to('regenerate your invoice', url=h.url_for(controller='registration', action='pay', id=c.signed_in_person.registration.id)) } for more details, go to the
${ h.link_to('registration status page', url=h.url_for(controller='register', action='status')) } or ${ h.email_link_to(c.config.get('contact_email'), 'contact the committee') } to clear up the situation.</p>
