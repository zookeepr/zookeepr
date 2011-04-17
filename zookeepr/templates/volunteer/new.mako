<%inherit file="/base.mako" />

<h2>Volunteer</h2>

${ h.form(h.url_for()) }
<%include file="form.mako" />
<p>${ h.submit("submit", "New") }
${ h.end_form() }
