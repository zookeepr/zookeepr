<%inherit file="/base.mako" />

<h2>View proposal type</h2>

<p>
   <b>Name:</b>
    ${ c.proposal_type.name | h }<br>
   <b>Notify Email:</b>
    ${ c.proposal_type.notify_email | h }<br>

</p>

${ h.link_to('Edit', url=h.url_for(action='edit',id=c.proposal_type.id)) } |
${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
