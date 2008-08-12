<h2>Reviews Summary</h2>

<div class="contents"><h3>Review Pages</h3>
<ul>
<li><a href="/review/help">How to review</a></li>
<li><% h.link_to('Review proposals', url=h.url(controller='proposal', action='review_index')) %></li>
<li><% h.link_to('Your reviews', url=h.url(controller='review', action='index')) %></li>
<li><% h.link_to('Summary of proposals', url=h.url(controller='proposal', action='summary')) %></li>
<li><% h.link_to('Reviewer summary', url=h.url(controller='review', action='summary')) %></li>
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
