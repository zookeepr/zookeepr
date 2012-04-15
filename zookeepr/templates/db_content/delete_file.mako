<%inherit file="/base.mako" />
<%
no_theme = 'true' if c.no_theme else 'false'
%>
${ h.form(url='/db_content/delete_file?file=' + c.file + '&folder=' + c.current_folder + '&no_theme=' + no_theme) }
<p>
Are you sure you want to delete this file?<br>
${ h.submit('submit', 'Yes, delete') }
</p>

${ h.end_form() }

