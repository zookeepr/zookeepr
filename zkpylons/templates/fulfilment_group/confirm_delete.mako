<%inherit file="/base.mako" />

<h2>Delete Fulfilment Status</h2>

${ h.form(h.url_for()) }

<p> Are you sure you want to delete this Fulfilment Status?</p>

<p>${ h.submit('submit', 'Delete') }
 or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>

${ h.end_form() }
