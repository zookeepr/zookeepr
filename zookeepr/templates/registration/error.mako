<%inherit file="/base.mako" />

<p>The following error has occured with your registration request:</p>
<p class="error-message">${ c.error }</p>
<p>Please return to the ${ h.link_to('registration status page', url=h.url_for(action='status')) }.</p>
