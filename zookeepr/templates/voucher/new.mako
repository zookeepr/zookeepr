<%inherit file="/base.mako" />

${ h.form(h.url(), multipart=True) }
<%include file="form.mako" />
${ h.submit('Add!', 'Add!') }
${ h.end_form() %> }

<%method title>
Voucher Code - <& PARENT:title &>
</%method>
