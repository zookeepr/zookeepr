<& head.myt &>

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form action="<% h.url_for('submission') %>" method="post" >

<& forms/person.myt &>
<& forms/address.myt &>
<& forms/profile.myt &>

<input type="submit" value="Submit"/>

</form>
</&>

<& tail.myt &>

<%args>
defaults
errors
</%args>