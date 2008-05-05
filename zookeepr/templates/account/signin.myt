<h1 class="pop">Sign in</h1>

<p>Don't have an account? <% h.link_to('Sign up', url=h.url(controller='account', action='new')) %> now!</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for(controller='/account', action='signin')) %>

	<p class="label"><label for="email_address">Email address:</label></p>
	<p class="entries"><% h.text_field('email_address', size=60) %></p>

	<p class="label"><label for="password">Password:</label></p>
	<p class="entries"><% h.password_field('password') %></p>

	<p class="submit"><% h.submit('Sign in') %></p>

<% h.end_form() %>

</&>

<p>
<% h.link_to('Forgotten your password?', url=h.url(action='forgotten_password')) %>
</p>

<p>Note: this login is for the 2009 linux.conf.au website; we have not
carried over any earlier linux.conf.au login information, so you will need
to register anew.</p>


<%args>
defaults
errors
</%args>


<%init>
if 'url' in request.GET:
    session['sign_in_redirect'] = '/' + request.GET['url']
    session.save()
</%init>
