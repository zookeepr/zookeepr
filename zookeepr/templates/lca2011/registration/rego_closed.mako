<%inherit file="/base.mako" />

<h2>Registration closed</h2>

<p>Unfortunately, registration is now closed.</p>

<p>If you have a voucher code, please
${ h.link_to('edit your registration details', url=h.url_for(action='edit', id=c.signed_in_person.registration.id)) } and enter it.</p>

<p>You can also go to the ${ h.link_to('registration status page', url=h.url_for(action='status')) }.</p>
