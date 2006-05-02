you're creating a new submission

<&| MODULE:mylib:formfill, defaults=c.defaults, errors=c.errors &>
<form action="<% h.url_for(action='new') %>" method="post" >
<table>
<tr><td>Handle:</td><td> <input type="text" name="handle" /></td></tr>
<tr><td>email:</td><td> <input type="text" name="email" /></td></tr>
<tr><td>password:</td><td> <input type="password" name="password" /></td></tr>
<tr><td>url:</td><td> <input type="text" name="url" /></td></tr>
<tr><td>file:</td><td> <input type="file" /></td></tr>

<tr><td>type:</td><td>
% for st in c.submissiontypes:
<% h.radio_button('type', st.name) %>
<label for="type"><% st.name %></label><br />
% #endfor
</td></tr>

<tr><td>abstract:</td><td><textarea name="abstract"> FOO </textarea></td></tr>
<tr><td></td><td><input type="submit" value="insert arse" /></td></tr>
</table>
</form>
</&>
