<%inherit file="/base.mako" />

<h2>Delete Proposal Type</h2>

${ h.form(h.url_for()) }

<p> Are you sure you want to delete this proposal type?</p>

${ h.submit('submit', 'Delete') } or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }

${ h.end_form() } 
