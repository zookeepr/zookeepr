<%inherit file="/base.mako" />

<h2>Edit page</h2>
${ h.form(h.url(), multipart=True) }
<%include file="form.myt" />
${ h.end_form() }

<%def name="title()">
Edit page - ${ caller.title() }
</%def>
