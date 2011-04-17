<%inherit file="/base.mako" />

<h2>Delete Voucher</h2>

${ h.form(h.url_for()) }

<p> Are you sure you want to delete this voucher?</p>

<p>${ h.submit('submit', 'Delete') }
 or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>

${ h.end_form() }

<%def name="title()">
Voucher - Delete - 
 ${ parent.title() }
</%def>

