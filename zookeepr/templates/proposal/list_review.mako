<%inherit file="/base.mako" />
<% import random %>
<h2>Proposal List</h2>

<div class="contents"><h3>Review Pages</h3>
<ul>
<%include file="reviewer_sidebar.mako" />
</ul>
</div>

% if c.num_reviewers <= 0:
   <% c.num_reviewers = 1 %>
% endif
<p>Below is all of the proposals that you have not yet reviewed. To start, please click "review now".</p>
<p>You have reviewed ${ len(c.person.reviews) } out of your quota of  ${ c.num_proposals * 3 / c.num_reviewers }. </p>



% for pt in c.proposal_types:
<%
	collection = getattr(c, '%s_collection' % pt.name)
	random.shuffle(collection)
	collection.sort(cmp = lambda x, y: cmp(len(x.reviews), len(y.reviews)))


	min_reviews = 100
	for p in collection:
		if len(p.reviews) < min_reviews:
			min_reviews = len(p.reviews)
		elif not p.reviews:
			min_reviews = 0
		endif
	endfor
%>

<h2>${ pt.name }s (${ len(collection) })</h2>

<table class="list">

<tr>
<th>ID - Title</th>
<th>Submitter(s)</th>
<th>Submission Time</th>
<th>Number of reviews</th>
<th>Reviewed?</th>
</tr>

% 	for s in collection:
## don't show the row if we've already reviewed it
%		if not [ r for r in s.reviews if r.reviewer == c.signed_in_person ]:
<tr class="${ h.cycle('even', 'odd') }">
	<td>${ h.link_to("%s - %s" % (s.id, h.util.html_escape(s.title)), url=h.url_for(action='view', id=s.id)) }</td>
	<td>
% 		for p in s.people:

${ h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address or p.id, url=h.url_for(controller='person', action='view', id=p.id)) }
%	endfor
</td>

<td>
${ s.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") }
</td>
<td>
${ len(s.reviews) }
</td>

	<td>
%		if min_reviews < 3 and len(s.reviews) > min_reviews :
	<small>Review something with ${ min_reviews } reviews first;
	${ h.link_to("review anyway", url=h.url_for(action="review", id=s.id)) }
	</small>
%		else:
	${ h.link_to("Review now!", url=h.url_for(action="review", id=s.id)) }
%		endif
	</td>
</tr>
%		endif only unreviewed
% 	endfor collection
</table>

<br>

% endfor proposal types

<%def name="title()" >
Proposals - ${ title.caller() }
</%def>
