<%inherit file="/base.mako" />

<% import random %>
<% c.signed_in_person = h.signed_in_person() %>
<h2>Funding Applications You Haven't Reviewed</h2>

% if c.num_reviewers <= 0:
   <% c.num_reviewers = 1 %>
% endif
<p>Below is all of the funding applications that you have not yet reviewed. To start, please click "review now".</p>


<% import re %>

% for ft in c.funding_types:
<%
	collection = getattr(c, '%s_collection' % ft.name)
	random.shuffle(collection)
	collection.sort(cmp = lambda x, y: cmp(len(x.reviews), len(y.reviews)))
        simple_title = re.compile('([^a-zA-Z0-9])').sub('', ft.name) 


	min_reviews = 100
	for p in collection:
		if len(p.reviews) < min_reviews:
			min_reviews = len(p.reviews)
		elif not p.reviews:
			min_reviews = 0
		endif
	endfor
%>

<a name="${ simple_title }"></a>
<h2>${ ft.name } requests (${ len(collection) })</h2>

<table class="list">

<tr>
<th>ID</th>
<th>Submitter</th>
<th>Submission Time</th>
<th>Number of reviews</th>
<th>Reviewed?</th>
</tr>

% 	for s in collection:
## don't show the row if we've already reviewed it
%		if not [ r for r in s.reviews if r.reviewer == c.signed_in_person ]:
<tr class="${ h.cycle('even', 'odd') }">
	<td>${ h.link_to("%s" % (s.id), url=h.url_for(action='view', id=s.id)) }</td>
	<td>
${ h.link_to( s.person.fullname, url=h.url_for(controller='person', action='view', id=s.person.id)) }
        </td>
<td>
${ s.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") |n}
</td>
<td align="right">
${ len(s.reviews) }
</td>

	<td>
%		if min_reviews < 3 and len(s.reviews) > min_reviews :
	<small>Review something with ${ min_reviews } reviews first;
	${ h.link_to("review anyway", url=h.url_for(action="review", id=s.id)) }
	</small>
%		else:
	${ h.link_to("Review!", url=h.url_for(action="review", id=s.id)) }
%		endif
	</td>
</tr>
%		endif only unreviewed
% 	endfor collection
</table>

<br>

% endfor proposal types

<%def name="title()" >
Funding Applications you haven't reviewed - ${ parent.title() }
</%def>

<%def name="contents()">
<%
  menu = ''

  import re

  for ft in c.funding_types:
    simple_title = re.compile('([^a-zA-Z0-9])').sub('', ft.name) 
    menu += '<li><a href="#' + simple_title + '">' + ft.name + ' requests</a></li>' 
  return menu
%>
</%def>

