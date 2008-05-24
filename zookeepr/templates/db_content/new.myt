<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.submit('Add!') %>
<% h.end_form() %>
</&>

<%method title>
New page - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
if not defaults:
  defaults = {
    'voucher_code.count': '1',
    'voucher_code.percentage': '100',
    'voucher_code.type': 'Professional',
  }

</%init>
