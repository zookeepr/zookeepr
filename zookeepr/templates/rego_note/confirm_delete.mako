<%inherit file="/base.mako" />

${ h.form(url=h.url_for()) }
<p>
Are you sure you want to delete this note?<br/>
${ h.submit('submit', 'Yes, delete') }
</p>

${ h.end_form() }

