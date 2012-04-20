<%inherit file="/base.mako" />

<h2>Voting page</h2>
${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />
${ h.end_form() }

<%def name="title()">
Voting page - ${ parent.title() }
</%def>
