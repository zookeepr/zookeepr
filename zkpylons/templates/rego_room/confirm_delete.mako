<%inherit file="/base.mako" />

${ h.form(url=h.url_for()) }
<h2>Delete Rego Room</h2>
<p>
Are you sure you want to delete this room detail?<br/>
${ h.submit('submit', 'Yes, delete') }
 or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>

<%include file="view_fragment.mako" />

${ h.end_form() }
