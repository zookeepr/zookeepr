    <h1>Edit registration</h1>

    <div id="registration">

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
    for k in ['shell', 'editor', 'distro', 'nick', 'prevlca', 'diet', 'special', 'miniconf', 'opendaydrag', 'checkin', 'checkout', 'partner_email', 'lasignup', 'silly_description', 'announcesignup', 'delegatesignup', 'speaker_record', 'speaker_video_release', 'speaker_slides_release']:
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
  <script type="text/javascript">
    function toggle_select_hidden(select, field) {
      if ( document.getElementById(select).value == 'other' ) {
        document.getElementById(field).style.display = 'inline';
      } else {
        document.getElementById(field).style.display = 'none';
      }
    }

    function silly_description() {
        path = "/registration/silly_description";
        xmlHttp = XMLHTTPObject();
        xmlHttp.open("POST", path, false);
        xmlHttp.send(null);
        response = xmlHttp.responseText;
        response_array = response.split(',');
        document.getElementById('silly_description').textContent = response_array[1];
        document.getElementById('registration.silly_description').value = response_array[1];
        document.getElementById('registration.silly_description_checksum').value = response_array[0];
    }

    function XMLHTTPObject() {
        var xmlhttp;
        if (window.ActiveXObject) {
            // Instantiate the latest Microsoft ActiveX Objects
            if (_XML_ActiveX) {
                xmlhttp = new ActiveXObject(_XML_ActiveX);
            } else {
                // loops through the various versions of XMLHTTP to ensure we're using the latest
                var versions = ["MSXML2.XMLHTTP", "Microsoft.XMLHTTP", "Msxml2.XMLHTTP.7.0", "Msxml2.XMLHTTP.6.0", "Msxml2.XMLHTTP.5.0", "Msxml2.XMLHTTP.4.0", "MSXML2.XMLHTTP.3.0"];
                for (var i = 0; i < versions.length ; i++) {
                    try {
                        // Try and create the ActiveXObject for Internet Explorer, if it doesn't work, try again.
                        xmlhttp = new ActiveXObject(versions[i]);
                        if (xmlhttp) {
                            var _XML_ActiveX = versions[i];
                            break;
                        }
                    } catch (e) {
                    // TRAP
                    };
                };
            }
        }
        // Well if there is no ActiveXObject available it must be firefox, opera, or something else
        if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
            try {
                xmlhttp = new XMLHttpRequest();
            } catch (e) {
                xmlhttp = false;
            }
        }
        return xmlhttp;
    }
  </script>
</%method>
