<%inherit file="/base.mako" />

    <h2>View Travel</h2>

    <p><b>Person:</b> ${ h.link_to(c.travel.person.fullname(), h.url_for(controller='person', action='view', id=c.travel.person.id)) }<br></p>
    <p><b>Origin Airport:</b> ${ c.travel.origin_airport }<br></p>
    <p><b>Destination Airport:</b> ${ c.travel.destination_airport }<br></p>



% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
