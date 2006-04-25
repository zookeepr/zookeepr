<%flags>
	inherit="/layout.myt"
</%flags>
<%args>
defaults
errors
</%args>

you're creating a new submission

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form action="<% h.url_for(action='new') %>" method="post" >
<table>
<tr><td>Handle:</td><td> <input type="text" name="handle" /></td></tr>
<tr><td>email:</td><td> <input type="text" name="email" /></td></tr>
<tr><td>password:</td><td> <input type="password" name="password" /></td></tr>
<tr><td>url:</td><td> <input type="text" name="url" /></td></tr>
<tr><td>file:</td><td> <input type="file" /></td></tr>
<tr><td>type:</td><td>
Paper: <input type="radio" name="type" value="Paper"><br />
Peer review paper: <input type="radio" name="type" value="Peer reviewed paper"><br />
BOF: <input type="radio" name="type" value="BOF"><br />
Miniconf: <input type="radio" name="type" value="Miniconf"><br />


<tr><td>abstract:</td><td><textarea name="abstract"> FOO </textarea></td></tr>
<tr><td></td><td><input type="submit" value="insert arse" /></td></tr>
</table>
</form>
</&>
