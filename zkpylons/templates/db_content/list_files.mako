<%inherit file="/base.mako" />
<%
no_theme = 'true' if c.no_theme else 'false'
%>
<h2>File manager</h2>

<p>Below is a list of files available from the root directory /. If you upload a file, you can access it with /current_folder/file_name.png</p>

<h3>Current folder: ${ c.current_path }</h3>

<table>
    <tr>
        <th>Icon/type</th>
        <th>Path</th>
        <th>Actions</th>
    </tr>
% if c.current_path is not '/' and c.current_path is not None and c.current_path is not '': #this doesn't work for who knows why!
    <tr>
        <td><img src="/images/icons/go-up.png" alt="[back icon]" title="folder"></td>
        <td><a href="/db_content/list_files?folder=${ c.current_path.rsplit('/',2)[0] + "/" }&no_theme=${ no_theme }">.. (Up)</a></td>
        <td>&nbsp;</td>
    </tr>
% endif
% for folder in c.folder_list:
    <tr class="${ h.cycle('even', 'odd')}">
        <td><img src="/images/icons/folder.png" alt="[folder icon]" title="folder"></td>
        <td><a href="/db_content/list_files?folder=${ c.current_path + folder }&no_theme=${ no_theme }">${ folder }</a></td>
        <td><a href="/db_content/delete_folder?folder=${ c.current_path + folder }&current_path=${ c.current_path }&no_theme=${ no_theme }"><img src="/images/icons/user-trash.png" alt="Delete" title="Delete"></a></td>
   </tr>
% endfor
% for file in c.file_list:
    <tr class="${ h.cycle('even', 'odd')}">
        <td><img src="/images/icons/mimetypes/${ h.extension(file) }.png" alt="[${ h.extension(file) } icon]" title="${ h.extension(file) }"></td>
        <td><a href="${ c.download_path + file }">${ file }</a></td>
        <td><a href="/db_content/delete_file?file=${ c.current_path + file }&folder=${ c.current_path }&no_theme=${ no_theme }"><img src="/images/icons/user-trash.png" alt="Delete" title="Delete"></a></td>
   </tr>
% endfor
</table>

            <form action="/db_content/upload?folder=${ c.current_path }&no_theme=${ no_theme }" method="post" enctype="multipart/form-data">
            <p><img src="/images/icons/document-new.png"> Upload file to ${ c.current_path }: <input type="file" name="myfile" id="myfile" />
                         <input type="submit" name="submit" value="Upload" /></p>
            </form>
            <p class="note">There are no checks on files except for authentication. Please do not upload anything too large or malicious.</p>
            <form action="/db_content/list_files?folder=${ c.current_path }&no_theme=${ no_theme }" method="post" enctype="multipart/form-data">
            <p><img src="/images/icons/folder-new.png"> New folder: <input type="text" name="folder" id="folder" />
                         <input type="submit" name="submit" value="Create" /></p>
            </form>
            <p class="note">Please keep file names safe and not duplicated.</p>

<%def name="title()">
List of files -
 ${ parent.title() }
</%def>
