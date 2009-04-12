<%inherit file="/base.mako" />

${ h.form(url=h.url_for()) }
<p>
Are you sure you want to delete this note?<br/>
${ h.submit('submit', 'Yes, delete') }
</p>

<%include file="view_fragment.mako" />

${ h.end_form() }

