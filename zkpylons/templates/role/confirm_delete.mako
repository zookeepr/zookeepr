<%inherit file="/base.mako" />
<h1>Delete Role</h1>

${ h.form(h.url_for()) }
<p> Are you sure you want to delete the "${ c.role.name }" role (number
${c.role.id})?</p>
<p>${ h.hidden('delete', 'ok') }
${ h.submit('Delete', 'Delete') }
${ h.end_form() } or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>


