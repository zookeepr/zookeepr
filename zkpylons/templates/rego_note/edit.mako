<%inherit file="/base.mako" />

<h2>Edit Rego Note</h2>
${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />
${ h.end_form() }

<%def name="title()">
Edit page - ${ parent.title() }
</%def>
