<%inherit file="/base.mako" />

<h2>Add a new note</h2>
${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />
${ h.end_form() }

<%def name="title()">
New note - ${ caller.title() }
</%def>
