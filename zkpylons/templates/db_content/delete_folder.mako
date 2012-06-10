<%inherit file="/base.mako" />
<%
no_theme = 'true' if c.no_theme else 'false'
%>
${ h.form(url='/db_content/delete_folder?folder=' + c.folder + '&current_path=' + c.current_folder + '&no_theme=' + no_theme) }
<p>
Are you sure you want to delete this folder? You must clear it out before you can delete it.<br>
${ h.submit('Submit', 'Yes, delete') }
</p>

${ h.end_form() }

