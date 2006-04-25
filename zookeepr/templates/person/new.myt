<%flags>
	inherit="/layout.myt"
</%flags>
<%args>
defaults
errors
</%args>

you're creating a person

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>

<div class="new">
<form name="new_person" action="<% h.url_for(action='new') %>" method="post" >

<table>
<tr><td>Handle:</td><td> <input type="text" name="handle" /></td></tr>
<tr><td>email:</td><td> <input type="text" name="email_address" /></td></tr>
<tr><td>password:</td><td> <input type="password" name="password" /></td></tr>

<tr><td>First name:</td><td><input type="text" name="firstname" /></td></tr>
<tr><td>Last name:</td><td><input type="text" name="lastname" /></td></tr>
<tr><td>Phone number</td><td><input type="text" name="phone" /></td></tr>
<tr><td>Fax number</td><td><input type="text" name="fax" /></td></tr>

<tr><td></td><td><input type="submit" value="insert arse" /></td></tr>

</table>
</form>
</div>

</&>
