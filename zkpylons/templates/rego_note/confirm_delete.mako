<%inherit file="/base.mako" />

<h2>Delete Rego Note</h2>

${ h.form(url=h.url_for()) }
<p>
Are you sure you want to delete this note?<br/>
${ h.submit('submit', 'Yes, delete') }
 or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>

<%include file="view_fragment.mako" />

${ h.end_form() }
