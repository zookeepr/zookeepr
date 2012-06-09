<%inherit file="/base.mako" />

<h2>Summary of Reviewers</h2>

<table>
  <tr>
    <th>Reviewer</th>
    <th>Number of Reviews</th>
% if h.auth.authorized(h.auth.Or(h.auth.has_organiser_role, h.auth.has_papers_chair_role)):
    <th>Avg Score</th>
% endif
  </tr>
% for reviewer in c.summary:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ reviewer[0].firstname } ${ reviewer[0].lastname }</td>
    <td>${ reviewer.count }</td>
%   if h.auth.authorized(h.auth.Or(h.auth.has_organiser_role, h.auth.has_papers_chair_role)):
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


