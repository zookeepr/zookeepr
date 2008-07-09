<h2>File manager</h2>
<h3>Current folder: <% c.current_path %></h3>

<table>
    <tr>
        <th>Icon/type</th>
        <th>Path</th>
        <th>Actions</th>
    </tr>
% if c.current_path is not '/' and c.current_path is not None and c.current_path is not '': #this doesn't work for who knows why!
    <tr>
        <td><img src="/images/icons/back.png" alt="[back icon]" title="folder"></td>
        <td><a href="/db_content/list_files?folder=<% c.current_path.rsplit('/',2)[0] + "/" %>">.. (Up)</a></td>
        <td>&nbsp;</td>
    </tr>
% #endif
% for folder in c.folder_list:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><img src="/images/icons/folder.png" alt="[folder icon]" title="folder"></td>
        <td><a href="/db_content/list_files?folder=<% c.current_path + folder %>"><% folder %></a></td>
        <td><a href="/db_content/delete_file?folder=<% c.current_path + folder %>">Delete</a></td>
   </tr>
% #endfor
% for file in c.file_list:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><img src="/images/icons/<% h.extension(file) %>.png" alt="[<% h.extension(file) %> icon]" title="<% h.extension(file) %>"></td>
        <td><a href="<% c.download_path + file %>"><% file %></a></td>
        <td><a href="/db_content/delete_file?file=<% c.current_path + file %>&folder=<% c.current_path %>">Delete</a></td>
   </tr>
% #endfor
</table>

            <form action="/db_content/upload?folder=<% c.current_path %>" method="post" enctype="multipart/form-data">
            <p>Upload file to <% c.current_path %>: <input type="file" name="myfile" id="myfile" />
                         <input type="submit" name="submit" value="Upload" /></p>
            </form>

<%method title>
List of Files - <& PARENT:title &>
</%method>

<%init>
</%init>
