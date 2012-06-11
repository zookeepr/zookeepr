<%inherit file="/base.mako" />

${ h.form(url=h.url_for(), multipart=True) }

<p><label for="attachment">Attach a file:</label>
<br>

${ h.file('attachment', size=50) }

<br>

${ h.submit('Upload', 'Upload') }
</p>
${ h.end_form() }


