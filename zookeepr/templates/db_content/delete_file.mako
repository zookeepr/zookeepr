<%inherit file="/base.mako" />

${ h.form(url='/db_content/delete_file?file=' + c.file + '&folder=' + c.current_folder) }
<p>
Are you sure you want to delete this file?<br>
${ h.submit('submit', 'Yes, delete') }
</p>

${ h.end_form() }

