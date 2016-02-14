<%inherit file="/base.mako" />

<h2>Edit Funding Type</h2>

${ h.form(h.url_for(id=c.funding_type.id)) }
<%include file="form.mako" />
${ h.submit('submit', 'Update') }
${ h.end_form() }
${ h.link_to('back', url=h.url_for(action='index', id=None)) }
