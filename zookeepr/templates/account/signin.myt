<h1 class="pop">Sign in</h1>

<p>Don't have an account? <% h.link_to('Sign up', url=h.url(controller='account', action='new')) %> now!</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for(controller='/account', action='signin')) %>

<table class="form" summary="sign-in form">
<tr>
	<th class="labels"><label for="email_address">Email address:</label></th>
	<td class="entries"><% h.text_field('email_address') %></td>
</tr>

<tr>
	<th class="labels"><label for="password">Password:</label></th>
	<td class="entries"><% h.password_field('password') %></td>
</tr>

<tr>
	<td></td>
	<td class="submit"><% h.submit('Sign in') %></td>
</tr>
</table>

<% h.end_form() %>

</&>

<p>
<% h.link_to('Forgotten your password?', url=h.url(action='forgotten_password')) %>
</p>

<%args>
defaults
errors
</%args>


<%init>
if 'url' in request.GET:
    session['sign_in_redirect'] = '/' + request.GET['url']
    session.save()
</%init>
