<%inherit file="/base.mako" />
<h1>Delete Content</h1>

${ h.form(h.url_for()) }
<p> Are you sure you want to delete the "${ c.db_content.title }" page (number
${c.db_content.id})?</p>
<p>${ h.hidden('delete', 'ok') }
${ h.submit('Delete', 'Delete') }
${ h.end_form() } or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>
