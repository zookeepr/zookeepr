<h1 class="pop">Sign out</h1>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for(controller='/account', action='signout')) %>

<table class="form" summary="sign-out form">

<tr>
	<td></td>
	<td class="submit"><% h.submit('Sign out') %></td>
</tr>
</table>

<% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>


<%init>
if 'url' in request.GET:
    session['sign_in_redirect'] = '/' + request.GET['url']
    session.save()
</%init>
