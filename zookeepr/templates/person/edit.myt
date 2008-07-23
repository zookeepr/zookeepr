<h2>Edit person</h2>

<p class="label">If you need to change your password you may <a href="/person/forgotten_password">reset it here</a>. We would like to avoid the changing of email addresses, however if you require your account email address to be updated, please contact <% h.webmaster_email() %>.</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url(id=c.person.id)) %>
<& form.myt &>
<p><% h.submitbutton('Update') %></p>
<% h.end_form() %>
</&>

<%args>
defaults
errors
</%args>

<%init>
c.form = 'edit'

# working around a bug in formencode, we need to set the defaults to
# the values in c.person
if not defaults:
    defaults = {}

    for k in ['email_address', 'firstname', 'lastname', 'address1', 'address2', 'city', 'state', 'postcode', 'country', 'company', 'phone', 'mobile']:
        v = getattr(c.person, k)
        if v is not None:
            defaults['person.' + k] = getattr(c.person, k)
</%init>
