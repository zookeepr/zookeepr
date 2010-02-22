<%inherit file="/base.mako" />

    <h2>View stream</h2>

    <p><b>Name:</b> ${ c.stream.name }<br></p>

    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.stream.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
