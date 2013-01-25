<%inherit file="/base.mako" />

<h2>Summary of Funding Reviewers</h2>

<%
review_summary = {}
for r in c.review_collection:
    if r.score is not None:
        if r.reviewer in review_summary:
            review_summary[r.reviewer]['num_reviews'] += 1
            review_summary[r.reviewer]['total_score'] += r.score
        else:
            review_summary[r.reviewer] = {}
            review_summary[r.reviewer]['num_reviews'] = 1
            review_summary[r.reviewer]['total_score'] = r.score
%>

<table>
<tr>
<th>Reviewer</th>
<th>Number of Funding Reviews</th>
% if h.auth.authorized(h.auth.has_organiser_role):
<th>Avg Score</th>
% endif
</tr>
% for reviewer in review_summary:
<tr class="${ h.cycle('even', 'odd') }">
<td>
${ reviewer.fullname }
</td>

<td>
${ review_summary[reviewer]['num_reviews'] }
</td>

%   if h.auth.authorized(h.auth.has_organiser_role):
<td>
<% avg = review_summary[reviewer]['total_score']*1.0/review_summary[reviewer]['num_reviews'] %>
${ "%#.*f" % (2, avg) }
</td>
%   endif

% endfor
</table>

<%def name="title()" >
Summary of Funding Reviewers - ${ parent.title() }
</%def>


