<%inherit file="/base.mako" />
<h1>View proposal type</h1>

<p>
   <b>Name:</b>
    ${ c.role.name | h }<br>
</p>

<p>
${ h.link_to('Edit', url=h.url_for(action='edit',id=c.role.id)) } |
${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
