<%inherit file="/base.mako" />

<h2>Add a new note</h2>
${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
<p>${ h.submit('submit', 'Save') }
${ h.link_to('Back', url=h.url_for(action='index')) }</p>
${ h.end_form() }

<%def name="title()">
New note - ${ caller.title() }
</%def>
