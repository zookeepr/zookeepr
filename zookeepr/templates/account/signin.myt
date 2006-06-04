<h1>Sign in!</h1>

<p>Don't have an account? <% h.link_to('Sign up', url=h.url(controller='person', action='new')) %> now!</p>

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

<%method title>
Sign in! - <& PARENT:title &>
</%method>
