<%inherit file="/base.mako" />

<h1>Edit role</h1>

${ h.form(h.url_for()) }
<%include file="form.mako" />
<p>${ h.submit('Update', 'Update') } - ${ h.link_to('back', url=h.url_for(action='index', id=None)) }</p>
${ h.end_form() }
