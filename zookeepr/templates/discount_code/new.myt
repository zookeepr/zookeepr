<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.submit('Add!') %>
<% h.end_form() %>
</&>

<%method title>
Discount Code - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
if not defaults:
  defaults = {
    'discount_code.count': '1',
    'discount_code.percentage': '100',
    'discount_code.type': 'Professional',
  }

</%init>
