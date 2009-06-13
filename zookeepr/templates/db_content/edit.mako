<%inherit file="/base.mako" />
<h2>Edit page</h2>

${ h.form(h.url_for()) }
<%include file="form.mako" />
${ h.end_form() }

<%def name="title()">
Edit Page -
 ${ parent.title() }
</%def>
