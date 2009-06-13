<%inherit file="/base.mako" />
<%namespace file="../proposal/reviewer_sidebar.mako" name="sidebar" inheritable="True"/>
<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
  ${ self.sidebar.toolbox_extra() }
</%def>

<h2>Reviews Summary</h2>

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
<% avg = review_summary[reviewer]['total_score']*1.0/review_summary[reviewer]['num_reviews'] %>
${ "%#.*f" % (2, avg) }
</td>

% endfor
</table>

<%def name="title()" >
Review Summary - ${ parent.title() }
</%def>


