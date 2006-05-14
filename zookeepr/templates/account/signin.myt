<h1>Sign In</h1>

<% c.form.start(name="signin", action=h.url_for(controller='/account', action='signin'), method="POST") %>
<% c.form.layout.simple_start() %>
<% c.form.layout.entry(
    content=c.form.field.text(name="username"),
    name='Username',
    error=c.form.get_error('username') ) %>
<% c.form.layout.entry(
    content=c.form.field.password(name="password", value=''),
    name='Password',
    error=c.form.get_error('password') ) %>
<% c.form.layout.entry(content=c.form.field.submit(name="go", value="Submit")) %>
<% c.form.layout.simple_end() %>
<% c.form.end() %>
