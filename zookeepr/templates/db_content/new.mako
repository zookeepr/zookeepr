<%inherit file="/base.mako" />
<h2>Add a new page</h2>


${ h.form(h.url_for()) }
<%include file="form.mako" />
${ h.end_form() }


<%def name="title()">
New Page - ${ parent.title() }
</%def>
