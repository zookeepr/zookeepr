<%inherit file="/base.mako" />

<h2>New Product</h2>

${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
<p>${ h.submit('submit', "New") }
${ h.link_to('Back', url=h.url_for(action='index')) }</p>
${ h.end_form() }
