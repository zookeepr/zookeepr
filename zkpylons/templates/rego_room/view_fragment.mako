<p><b>For registration:</b> </p>
${ h.link_to(c.rego_room.rego.person.fullname, h.url_for(controller='person',
action='view', id=c.rego_room.rego.person.id)) },
${ h.link_to('View Registration', h.url_for(controller='registration', action='view', id=c.rego_room.rego.id)) }</p>
<p><b>By:</b> ${ h.link_to(c.rego_room.by.fullname, h.url_for(controller='person',
action='view', id=c.rego_room.by.id)) },

<p><b>Room number:</b> ${ c.rego_room.room }</p>

<p>${ h.link_to('Edit', h.url_for(controller='rego_room', action='edit',
id=c.rego_room.id)) } | ${ h.link_to('Back', h.url_for(controller='rego_room', action='index')) }</p>

<%def name="title()">
View room - ${ parent.title() }
</%def>
