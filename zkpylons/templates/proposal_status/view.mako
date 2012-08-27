<%inherit file="/base.mako" />

    <h2>View Proposal Status</h2>

    <p><b>Name:</b> ${ c.proposal_status.name }<br></p>

% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
