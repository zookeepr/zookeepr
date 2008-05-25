<h1>Edit registration</h1>

<div id="registration">

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url()) %>

<h2>About yourself</h2>

<p class="label">
<label for="person.firstname">Your first name:</label></p>
<p>
<% c.registration.person.firstname | h %>
</p>

<p class="label">
<label for="person.lastname">Your last name:</label></p>
<p>
<% c.registration.person.lastname | h %>
</p>

<p class="label">
<label for="person.email_address">Email address:</label></p>
<p>
<% c.registration.person.email_address | h %>
</p>
<p class="note">
Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.
</p>

</fieldset>

<& form.myt &>
<p class="submit"><% h.submit('Update') %></p>
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
    for k in ['shell', 'shelltext', 'editor', 'editortext', 'distro', 'distrotext', 'nick', 'prevlca', 'type', 'voucher_code', 'teesize', 'extra_tee_count', 'extra_tee_sizes', 'dinner', 'diet', 'special', 'miniconf', 'opendaydrag', 'accommodation', 'checkin', 'checkout', 'partner_email', 'kids_0_3', 'kids_4_6', 'kids_7_9', 'kids_10_11', 'kids_12_17', 'pp_adults', 'speaker_pp_pay_adult', 'speaker_pp_pay_child', 'lasignup', 'announcesignup', 'delegatesignup', 'speaker_record', 'speaker_video_release', 'speaker_slides_release']:
        v = getattr(c.registration, k)
        if v is not None:
            defaults['registration.' + k] = getattr(c.registration, k)

    for k in ['address1', 'address2', 'city', 'state', 'postcode', 'country']:
        v = getattr(c.registration.person, k)
        if v is not None:
            defaults['person.' + k] = getattr(c.registration.person, k)

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

    if c.registration.speaker_record:
        defaults['registration.speaker_record'] = 1
    else:
        defaults['registration.speaker_record'] = 0
    if c.registration.speaker_video_release:
        defaults['registration.speaker_video_release'] = 1
    else:
        defaults['registration.speaker_video_release'] = 0
    if c.registration.speaker_slides_release:
        defaults['registration.speaker_slides_release'] = 1
    else:
        defaults['registration.speaker_slides_release'] = 0


    if c.registration.miniconf:
        for mc in c.registration.miniconf:
            defaults['registration.miniconf.' + mc] = 1
            if mc == 'OpenOffice':
                defaults['registration.miniconf.OpenOffice.org'] = 1
    if c.registration.prevlca:
        for p in c.registration.prevlca:
            defaults['registration.prevlca.' + p] = 1

</%init>
