<%inherit file="/base.mako" />

<h2>Viewing note</h2>

<p><b>For registration:</b> </p>
<p><b>By:</b> ${ h.link_to(c.rego_note.rego.person.firstname + ' ' + c.rego_note.rego.person.lastname, h.url_forcontroller='person', action='view', id=c.rego_note.rego.person.id)) }, ${ h.link_to('View Registration', h.url_forcontroller='registration', action='view', id=c.rego_note.rego.id)) }</p>

<p><b>Note:</b> ${ c.rego_note.note }</p>

<p>${ h.link_to('Edit', h.url_forcontroller='rego_note', action='edit', id=c.rego_note.id)) } | ${ h.link_to('Back', h.url_forcontroller='rego_note', action='index')) }</p>

<%def name="title()">
View note - ${ caller.title() }
</%def>
