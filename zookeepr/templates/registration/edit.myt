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
	for k in ['address1', 'address2', 'city', 'state', 'country', 'postcode', 'phone', 'company', 'shell', 'shelltext', 'editor', 'editortext', 'distro', 'distrotext', 'prevlca', 'type', 'discount_code', 'teesize', 'dinner', 'diet', 'special', 'miniconf', 'accommodation', 'checkin', 'checkout', 'partner_email', 'kids_0_3', 'kids_4_6', 'kids_7_9', 'kids_10', 'lasignup', 'announcesignup', 'delegatesignup']:
		v = getattr(c.registration, k)
		if v is not None:
			defaults['registration.' + k] = getattr(c.registration, k)
	# FIXME: UGH durty hack
	if c.registration.accommodation:
		defaults['registration.accommodation'] = c.registration.accommodation.id
	if c.registration.lasignup:
		defaults['registration.lasignup'] = 1
	else:
		defaults['registration.lasignup'] = 0
	if c.registration.announcesignup:
		defaults['registration.announcesignup'] = 1
	else:
		defaults['registration.announcesignup'] = 0
	if c.registration.delegatesignup:
		defaults['registration.delegatesignup'] = 1
	else:
		defaults['registration.delegatesignup'] = 0

	if c.registration.miniconf:
		for mc in c.registration.miniconf:
			defaults['registration.miniconf.' + mc] = 1
			if mc == 'OpenOffice':
				defaults['registration.miniconf.OpenOffice.org'] = 1
	if c.registration.prevlca:
		for p in c.registration.prevlca:
			defaults['registration.prevlca.' + p] = 1

</%init>
