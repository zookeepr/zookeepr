# myform.myt
<html>
<head><title>basic form</title></head>

<body>

<&| MODULE:mylib:formfill, defaults=defaults, errors=errors &>
<form action="/register" method="post">
Username: <input type="text" name="username" size="26" />
<form:error name="username">
Age: <input type="text" name="age" size="3" />
<form:error name="age">
<input type="submit" value="Send it" />
</form>
</&>

</body>
</html>

<%args>
defaults
errors
</%args>
