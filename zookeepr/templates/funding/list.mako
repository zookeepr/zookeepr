<%inherit file="/base.mako" />

<h2>My Funding Applications</h2>

% if len(c.person.funding) > 0:

%  if c.funding_editing == 'closed':
<p>Funding editing has been disabled while the review committee assess your
proposals.</p>
%  endif
<p>Below is a list of funding requests you have submitted. To view one click
on the view link; or to edit, click on the edit link.</p>
<table>
  <tr class="odd">
    <th>Proposal Type</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%   for s in c.person.funding:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ s.type.name }</td>
    <td>
%     if s.status.name == 'Pending':
        <i>Undergoing review</i>
%     elif s.status.name == 'Accepted':
        Accepted</p>
%     elif s.status.name == 'Withdrawn':
        Withdrawn
%     else:
        Declined
%     endif
    </td>
    <td>
      ${ h.link_to("view", url=h.url_for(action='view', id=s.id)) }
%if s.status.name == 'Pending' or s.status.name == 'Accepted':
%  if c.funding_editing == 'open':
  ${ h.link_to("edit", url=h.url_for(controller='funding', action='edit', id=s.id)) }
%  endif
${ h.link_to("withdraw", url=h.url_for(controller='funding', action='withdraw', id=s.id)) }
    </td>
  </tr>
%endif
% endfor
</table>

%else:
    <p>You haven't submitted any funding application requests.</p>
%endif

<p><ul>
%  if c.funding_status == 'open':
<li>${ h.link_to('New funding request', url=h.url_for(controller='funding', action='new')) }</li>
%  endif
</ul></p>

<%def name="short_title()"><%
  return 'My Funding Applications'
%>
</%def>
<%def name="title()">
My Funding Applications - ${ parent.title() }
</%def>

