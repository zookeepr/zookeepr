<h2 class="pop">New user account creation</h2>

<p>This form is for creating an account on linux.conf.au. After you have created an account you may submit a miniconf or presentation from the Programme/Participate menu.</p>

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
