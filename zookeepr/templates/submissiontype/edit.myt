<%args>
defaults
errors
</%args>

Edit submission type

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form name="edit_subtype" action="<% h.url_for(action='edit') %>" method="post" >

<div class="formlabel">Name:</div>
<div class="formfield"><input type="text" name="name" /></div>

<div class="submit"><input type="submit" value="Submit" /></div>

</form>
</&>
