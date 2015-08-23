<%inherit file="/base.mako" />

<h2>Summary of Reviewers</h2>

<table class="table sortable">
  <tr>
    <th>Reviewer</th>
    <th>Reviews</th>
    <th>Declined</th>
% if h.auth.authorized(h.auth.Or(h.auth.has_organiser_role, h.auth.has_proposals_chair_role)):
    <th>Avg Score</th>
% endif
  </tr>
% for reviewer in c.summary:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ reviewer.Person.firstname } ${ reviewer.Person.lastname }</td>
    <td>${ reviewer.reviews }</td>
    <td>${ reviewer.declined }</td>
%   if h.auth.authorized(h.auth.Or(h.auth.has_organiser_role, h.auth.has_proposals_chair_role)):
%     if reviewer.average is None:
    <td>No Average</td>
%     else:
    <td>${ "%#.*f" % (2, reviewer.average) }</td>
%     endif
%   endif
  </tr>
% endfor
</table>

<%def name="title()" >
Summary of Reviewers - ${ parent.title() }
</%def>


