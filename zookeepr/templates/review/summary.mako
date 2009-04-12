<%inherit file="/base.mako" />

<h2>Reviews Summary</h2>

<div class="contents"><h3>Review Pages</h3>
<ul>
<%include file="../proposal/reviewer_sidebar.mako" />
</ul>
</div>

<%
review_summary = {}
for r in c.review_collection:
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
<th>Number of Reviews</th>
<th>Avg Score</th>
</tr>
% for reviewer in review_summary:
<tr class="${ h.cycle('even', 'odd') }">
<td>
${ reviewer.firstname }
${ reviewer.lastname }
</td>

<td>
${ review_summary[reviewer]['num_reviews'] }
</td>

<td>
${ review_summary[reviewer]['total_score']*1.0/review_summary[reviewer]['num_reviews'] }
</td>

% endfor
</table>

<%def name="title()" >
Review Summary - ${ caller.title() }
</%def>


