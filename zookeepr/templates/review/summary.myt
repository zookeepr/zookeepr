<h2>Reviews Summary</h2>

<div class="contents"><h3>Review Pages</h3>
<ul>
<& ../proposal/reviewer_sidebar.myt &>
</ul>
</div>

% review_summary = {}
% for r in c.review_collection:
%     if r.reviewer in review_summary:
%         review_summary[r.reviewer]['num_reviews'] += 1
%         review_summary[r.reviewer]['total_score'] += r.score
%     else:
%         review_summary[r.reviewer] = {}
%         review_summary[r.reviewer]['num_reviews'] = 1
%         review_summary[r.reviewer]['total_score'] = r.score
%     # endif
% # endfor

<table>
<tr>
<th>Reviewer</th>
<th>Number of Reviews</th>
<th>Avg Score</th>
</tr>
% for reviewer in review_summary:
<tr class="<% h.cycle('even', 'odd') %>">
<td>
<% reviewer.firstname %>
<% reviewer.lastname %>
</td>

<td>
<% review_summary[reviewer]['num_reviews'] |h %>
</td>

<td>
<% review_summary[reviewer]['total_score']*1.0/review_summary[reviewer]['num_reviews'] |h %>
</td>

% #endfor
</table>

<%method title>
Review Summary - <& PARENT:title &>
</%method>
