<%inherit file="/base.mako" />

    <h2>View Proposal Status</h2>

    <p><b>Name:</b> ${ c.proposal_status.name }<br></p>

% if c.proposal_status.proposals:
    <table>
      <tr>
        <th>&nbsp;</th>
        <th>Title</th>
      <tr>
%   for proposal in c.proposal_status.proposals:
      <tr>
        <td>${ h.link_to(proposal.id, h.url_for(controller='proposal', action='view', id=proposal.id)) }</td>
        <td>${ proposal.title }</td>
      </tr>
%   endfor
    </table>
% endif

% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
