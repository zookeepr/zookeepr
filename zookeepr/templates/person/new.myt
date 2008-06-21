<h1 class="pop">New user account creation</h1>

<p>
This form is only for selected personnelle that need an account for specific purposes. <b>To submit a proposal for the conference, <a href="/programme/submit_a_presentation">go
directly to this form</a></b>, don't bother with this one.</p>

<p>
If you've already got an account but can't log in, you can <% h.link_to('recover your password', url=h.url(controller='person',id=None,action='forgotten_password')) %>.
</p>

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
if not defaults:
    defaults = {
        'person.country': 'Australia',
    }
</%init>
