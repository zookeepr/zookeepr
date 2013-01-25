<%inherit file="/base.mako" />
<% c.signed_in_person = h.signed_in_person() %>
<%def name="toolbox_extra()">
% if h.auth.authorized(h.auth.has_organiser_role) or c.funding_editing == 'open' and c.signed_in_person == c.funding.person:
  <li>${ h.link_to('Edit Funding Application', url=h.url_for(controller='funding', action='edit',id=c.funding.id)) }</li>
% endif 
</%def>

<%def name="toolbox_extra_funding_reviewer()">
## Add review link if the signed in person is a funding reviewer, but not
## if they've already reviewed this proposal
% if h.url_for().endswith('review') is not True and h.url_for().endswith('edit') is not True:
  <li>${ h.link_to('Review this application', url=h.url_for(action='review')) }</li>
% endif
</%def>

<%def name="heading()">
  ${ c.funding.type.name }
</%def>

<% c.signed_in_person = h.signed_in_person() %>

<h2>${ self.heading() }</h2>


<%include file="view_fragment.mako" />

<hr>
<ul>
% if h.auth.authorized(h.auth.has_organiser_role) or c.funding_editing == 'open' and c.signed_in_person == c.funding.person:
  <li>${ h.link_to('Edit Funding Application', url=h.url_for(controller='funding', action='edit',id=c.funding.id)) }</li>
% endif 

## Add review link if the signed in person is a reviewer, but not if they've already reviewed this proposal
% if h.url_for().endswith('review') is not True and h.url_for().endswith('edit') is not True and 'funding_reviewer' in [x.name for x in c.signed_in_person.roles]:
<li>
${ h.link_to('Review this funding application', url=h.url_for(controller='funding', action='review')) }
</li>
% endif
</ul>

% if ('funding_reviewer' in [x.name for x in c.signed_in_person.roles]) or ('organiser' in [x.name for x in c.signed_in_person.roles]):
<h3>Reviews</h3>

%   if len(c.funding.reviews) == 0:
<table>
   <tr><td>No reviews</td></tr>
</table>
%   else:
<table>
<tr>
<th># - Reviewer</th>
<th>Score</th>
<th>Comment</th>
</tr>

%     for r in c.funding.reviews:
<tr class="${ h.cycle('even', 'odd') }">
<td style="vertical-align: top;">
${ h.link_to("%s - %s" % (r.id, r.reviewer.fullname), url=h.url_for(controller='funding_review', id=r.id, action='view')) }
</td>

<td style="vertical-align: top;">
${ r.score | h }
</td>

<td style="vertical-align: top;">
${ h.line_break(h.util.html_escape(r.comment)) | n}
</td>

</tr>
%     endfor
</table>
%   endif
% endif

${ next.body() }

