<%inherit file="/base.mako" />

${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />
${ h.submit('Add', 'Add') }
${ h.end_form() }

<%def name="title()" >
Voucher Code - ${ parent.title() }
</%def>

