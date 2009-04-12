<%inherit file="/base.mako" />

    <h1>Edit registration</h1>

    <div id="registration">

% if errors:
      <p class="error-message">There
%   if len(errors)==1:
      is one problem
%   else:
      are ${ `len(errors)` |h } problems
%   endif
      with your registration form, highlighted in red below. Please correct and re-submit.</p>
% endif

${ h.form(h.url()) }
<%include file="form.mako" />

        <p class="submit">${ h.submit('update','Update') }</p>
      ${ h.end_form() }

    </div>
<%init>
if not defaults:
    defaults = {}
    for k in ['shell', 'editor', 'distro', 'nick', 'keyid', 'planetfeed', 'prevlca', 'diet', 'special', 'miniconf', 'checkin', 'checkout', 'signup', 'silly_description', 'voucher_code']:
        v = getattr(c.registration, k)
        if v is not None:
            if k in ('shell', 'editor', 'distro') and v not in h.lca_rego[k + 's'] and v != '':
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
    if c.registration.over18:
        defaults['registration.over18'] = 1
    else:
        defaults['registration.over18'] = 0


    if c.registration.miniconf:
        for mc in c.registration.miniconf:
            defaults['registration.miniconf.' + mc] = 1
    if c.registration.prevlca:
        for p in c.registration.prevlca:
            defaults['registration.prevlca.' + p] = 1
    if c.registration.signup:
        for s in c.registration.signup:
            defaults['registration.signup.' + s] = 1

</%init>
