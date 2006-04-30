<%args>
defaults
errors
</%args>

New person

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form name="new_person" action="<% h.url_for(action='new') %>" method="post" >

<label for="handle">Handle:</label>
<input type="text" name="handle"/>

<label for="email_address">Email:</label>
<input type="text" name="email_address" />

<label for="password">Password:</label>
<input type="password" name="password" />

<label for="firstname">First name:</label>
<input type="text" name="firstname" />

<label for="lastname">Last name:</label>
<input type="text" name="lastname" />

<label for="phone">Phone number:</label>
<input type="text" name="phone" />

<label for="fax">Fax number:</label>
<input type="text" name="fax" />

<input type="submit" value="Submit" />
<input type="reset" value="Reset" />

</form>
</&>
