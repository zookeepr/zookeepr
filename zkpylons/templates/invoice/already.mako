<%inherit file="/base.mako" />
<h2>Invoice already ${ c.status }</h2>

<p>The invoice is marked as ${ c.status }. Please go to the <a
href="/register/status">registration status page</a> or
${ h.email_link_to(c.config.get('contact_email'), 'contact the committee') } to clear up the
situation.</p>

