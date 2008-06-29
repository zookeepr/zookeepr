<h2 class="pop">Would you like to sign out?</h2>
<p>Please confirm you would like to sign out.</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for(controller='/person', action='signout')) %>

	<p class="submit"><% h.submitbutton('Sign out') %></p>

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
