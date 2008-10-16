<h2>Veiwing note</h2>

<p><b>For registration:</b> </p>
<p><b>By:</b> <% h.link_to(c.rego_note.rego.person.firstname + ' ' + c.rego_note.rego.person.lastname, h.url(controller='person', action='view', id=c.rego_note.rego.person.id)) %>, <% h.link_to('View Registration', h.url(controller='registration', action='view', id=c.rego_note.rego.id)) %></p>

<p><b>Note:</b> <% c.rego_note.note %></p>

<p><% h.link_to('Edit', h.url(controller='rego_note', action='edit', id=c.rego_note.id)) %> | <% h.link_to('Back', h.url(controller='rego_note', action='index')) %></p>

<%method title>
View note - <& PARENT:title &>
</%method>

<%init>
</%init>
