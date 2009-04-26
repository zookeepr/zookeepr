<%inherit file="/base.mako" />

<h2>Delete attachment</h2>

${ h.form(h.url_for()) }

<p>Are you sure you want to delete this attachment?</p>

<p>${ h.submit('submit', 'Yes, delete') }</p>

${ h.end_form() }
