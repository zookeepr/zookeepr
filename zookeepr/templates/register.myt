<& head.myt &>

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form action="<% h.url_for('register', action='new') %>" method="post">
Username: <input type="text" name="username" size="26" />
<form:error name="username">
Age: <input type="text" name="age" size="3" />
<form:error name="age">
<input type="submit" value="Send it" />
</form>
</&>

<& tail.myt &>

<%args>
defaults
errors
</%args>
