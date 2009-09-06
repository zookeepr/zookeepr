<%inherit file="/base.mako" />

<h2>Delete attachment</h2>

${ h.form(h.url_for()) }

<p>Are you sure you want to delete this attachment?  Name: ${ c.attachment.filename }</p>

<p>${ h.submit('submit', 'Yes, delete') }
or ${ h.link_to('No, take me back.', url=h.url_for(controller='funding', action='view', id=c.funding.id)) }</p>

${ h.end_form() }
