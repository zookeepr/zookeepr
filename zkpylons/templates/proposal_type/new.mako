<%inherit file="/base.mako" />

<h2>New Proposal Type</h2>

${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
${ h.submit('submit', "New") }
${ h.end_form() }

${ h.link_to('Back', url=h.url_for(action='index')) }
