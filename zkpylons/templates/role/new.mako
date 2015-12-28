<%inherit file="/base.mako" />

<h1>New Role</h1>

${ h.form(h.url_for()) }
<%include file="form.mako" />
<p>${ h.submit("submit", "New") } - ${ h.link_to('Back', url=h.url_for(action='index')) }</p>
${ h.end_form() }
