<%inherit file="/base.mako" />
<h2>Old invoice</h2>

<p>This invoice is old; please 
${ h.link_to('regenerate the invoice', url=h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }
for maximum freshness.</p>

<p>You can also go to the <a href="/register/status">registration status page</a>.
