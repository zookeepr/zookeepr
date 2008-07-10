<% h.form(url='/db_content/delete_folder?folder=' + c.folder + '&current_path=' + c.current_folder) %>
<p>
Are you sure you want to delete this folder? You must clear it out before you can delete it.<br>
<% h.submitbutton('Yes, delete') %>
</p>

<% h.end_form() %>

