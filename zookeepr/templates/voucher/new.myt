<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
    <% h.form(h.url(), multipart=True) %>
<& form.myt &>
    <% h.submitbutton('Add!') %>
    <% h.end_form() %>
</&>

<%method title>
Voucher Code - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
if not defaults:
  defaults = {
    'voucher.count': '1',
    'voucher.percentage': '100',
    'voucher.type': 'Professional',
  }

</%init>
