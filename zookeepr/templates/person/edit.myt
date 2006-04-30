<%args>
defaults
errors
</%args>

Edit person

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form name="edit_person" action="<% h.url_for(action='edit') %>" method="post" >

<div class="formlabel">Name:</div>
<div class="formfield"><input type="text" name="name" /></div>

<div class="submit"><input type="submit" value="Submit" /></div>

</form>
</&>
