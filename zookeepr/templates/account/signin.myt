<h2>Sign in to your MyLCA</h2>

<p>Don't have an account? <% h.link_to('Sign up', url=h.url(controller='account', action='new')) %> now!</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for(controller='/account', action='signin')) %>

<p>
<label for="email_address">Email address:</label>
<% h.text_field('email_address') %>
</p>

<p>
<label for="password">Password:</label>
<% h.password_field('password') %>
</p>

<% h.submit('Sign in') %>

<% h.end_form() %>

</&>

<p>
<% h.link_to('Forgotten your password?', url=h.url(action='forgotten_password')) %>
</p>

<%method title>
Sign in to MyLCA - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>


<%init>
if 'url' in request.GET:
    session['sign_in_redirect'] = '/' + request.GET['url']
    session.save()
</%init>
