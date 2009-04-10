<h2 class="pop">New user account creation</h2>

<p>Enter your name, and email address, and password, and we'll email you with a confirmation to create your account.</p>

<p>
If you've already got an account but can't log in, you can <% h.link_to('recover your password', url=h.url(controller='person',id=None,action='forgotten_password')) %>.
</p>

<p><b>To register for the conference, <% h.link_to('go directly to the registration form', url=h.url(controller='registration', action='new')) %>, don't bother with this one.</b></p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<form method="post" id="login-form" action="<% h.url_for() %>" >

<& form.myt &>

<p class="submit"><% h.submitbutton("Create a new account") %></p>

</form>
</&>

<%args>
defaults
errors
</%args>
<%init>
c.form = 'new'

if not defaults:
    defaults = {
        'person.country': 'New Zealand',
    }
</%init>
