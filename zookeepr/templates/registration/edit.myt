    <h1>Edit registration</h1>

    <div id="registration">

% if errors:
      <p class="error-message">There
%   if len(errors)==1:
      is one problem
%   else:
      are <% `len(errors)` |h %> problems
%   #endif
      with your registration form, highlighted in red below. Please correct and re-submit.</p>
% #endif

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

      <% h.form(h.url()) %>
<& form.myt, defaults=defaults, errors=errors &>
        <p class="submit"><% h.submitbutton('Update') %></p>
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
#FIXME: Partner program
if not defaults:
    defaults = {}
    for k in ['shell', 'editor', 'distro', 'nick', 'prevlca', 'diet', 'special', 'miniconf', 'opendaydrag', 'checkin', 'checkout', 'lasignup', 'silly_description', 'voucher_code', 'announcesignup', 'delegatesignup', 'speaker_record', 'speaker_video_release', 'speaker_slides_release']:
        v = getattr(c.registration, k)
        if v is not None:
            if k in ('shell', 'editor', 'distro') and v not in h.lca_rego[k + 's']:
                defaults['registration.' + k] = 'other'
                defaults['registration.' + k + 'text'] = getattr(c.registration, k)
            elif k == 'silly_description':
                defaults['registration.' + k] = getattr(c.registration, k)
                defaults['registration.silly_description_checksum'] = h.silly_description_checksum(getattr(c.registration, k))
            else:
                defaults['registration.' + k] = getattr(c.registration, k)
    defaults['products.partner_email'] = getattr(c.registration, 'partner_email')

    for rproduct in c.registration.products:
        if rproduct.product and rproduct.product.category:
            if rproduct.product.category.display in ('radio', 'select'):
                defaults['products.category_' + str(rproduct.product.category.id)] = rproduct.product.id
            elif rproduct.product.category.display == 'checkbox':
                defaults['products.product_' + str(rproduct.product.id)] = 1
            elif rproduct.product.category.display == 'qty':
                defaults['products.product_' + str(rproduct.product.id) + '_qty'] = rproduct.qty

    for k in ['address1', 'address2', 'city', 'state', 'postcode', 'country', 'phone', 'mobile', 'company']:
        v = getattr(c.registration.person, k)
        if v is not None:
            defaults['person.' + k] = getattr(c.registration.person, k)

    # FIXME: UGH durty hack
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
    if c.registration.prevlca:
        for p in c.registration.prevlca:
            defaults['registration.prevlca.' + p] = 1

</%init>
<%method extra_head>
</%method>
