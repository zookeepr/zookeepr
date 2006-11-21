<h1>Edit registration</h1>

<div id="registration">

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url()) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>

</&>

</div>

<%args>
defaults
errors
</%args>

<%init>
# working around a bug in formencode, we need to set the defaults to
# the values in c.registration
if not defaults:
	defaults = {}
	for k in ['address1', 'address2', 'city', 'state', 'country', 'postcode', 'phone', 'company', 'shell', 'shelltext', 'editor', 'editortext', 'distro', 'distrotext', 'prevlca', 'type', 'discount_code', 'teesize', 'dinner', 'diet', 'special', 'miniconf', 'accommodation', 'checkin', checkout', 'partner_email', 'kids_0_3', 'kids_4_6', 'kids_7_9', 'kids_10', 'lasignup', 'announcesignup', 'delegatesignup']:
		defaults['registration.' + k] = getattr(c.registration, k)
</%init>
