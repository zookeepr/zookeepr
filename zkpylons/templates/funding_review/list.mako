<%inherit file="/base.mako" />

<h2>Your funding reviews</h2>

<table>
<tr>
<th>Name</th>
<th>Type</th>
<th>Score</th>
<th>Comment</th>
<th>Edit</th>
</tr>
% for r in c.review_collection:
%	if r.reviewer == h.signed_in_person():

<tr class="${ h.cycle('even', 'odd') }">

<td>
${ h.link_to("%s - %s" % (r.funding.id, r.funding.person.fullname ), url=h.url_for(controller='funding_review', action='view', id=r.id)) }
</td>

<td>
${ r.funding.type.name }

<td>
% if r.score is None:
abstain
% else:
${ r.score }
% endif
</td>

<td>
${ h.truncate(r.comment) }
</td>

<td>
${ h.link_to("edit", url=h.url_for(controller='funding_review', action='edit', id=r.id)) }&nbsp;-&nbsp;${ h.link_to("delete", url=h.url_for(controller='funding_review', action='delete', id=r.id)) }
</td>
</tr>

% 	endif
% endfor
</table>

<%def name="title()" >
Funding Reviews - ${ parent.title() }
</%def>

