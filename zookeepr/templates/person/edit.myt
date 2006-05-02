<%args>
defaults
errors
</%args>

Edit person

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form name="edit_person" action="<% h.url_for(action='edit') %>" method="post" >

<label for="handle">Handle:</label>
<input type="text" name="handle" />

<label for="email_address">Email address:</label>
<input type="text" name="email_address" />

<label for="firstname">First name:</label>
<input type="text" name="firstname" />

<label for="lastname">Last name:</label>
<input type="text" name="lastname" />

<label for="phone">Phone number:</label>
<input type="text" name="phone" />

<label for="fax">Fax:</label>
<input type="text" name="fax" />

<input type="submit" value="Submit" />
<input type="reset" value="Reset" />

</form>
</&>
