<%inherit file="/base.mako" />
<% c.signed_in_person = h.signed_in_person() %>
<%def name="toolbox_extra()">
%   if c.signed_in_person in c.proposal.people or h.auth.authorized(h.auth.has_organiser_role):
  <li>${ h.link_to('Edit Proposal', url=h.url_for(controller='proposal', action='edit',id=c.proposal.id)) }</li>
% endif 
</%def>

<%def name="toolbox_extra_reviewer()">
## Add review link if the signed in person is a reviewer, but not if they've already reviewed this proposal
% if h.url_for().endswith('review') is not True and h.url_for().endswith('edit') is not True:
  <li>${ h.link_to('Review this proposal', url=h.url_for(action='review')) }</li>
% endif
</%def>

<%def name="heading()">
  ${ c.proposal.title }
</%def>

<% c.signed_in_person = h.signed_in_person() %>

<h2>${ self.heading() }</h2>


<%include file="view_fragment.mako" />


% if c.signed_in_person in c.proposal.people or ('organiser' in [x.name for x in c.signed_in_person.roles]):
%     if c.paper_editing == 'open':
<ul><li>
${ h.link_to('Edit Proposal', url=h.url_for(controller='proposal', action='edit',id=c.proposal.id)) }
</li></ul>
%     endif
% endif


## Add review link if the signed in person is a reviewer, but not if they've already reviewed this proposal
% if h.url_for().endswith('review') is not True and h.url_for().endswith('edit') is not True and 'reviewer' in [x.name for x in c.signed_in_person.roles]:
<ul><li>
${ h.link_to('Review this proposal', url=h.url_for(action='review')) }
</li></ul>
% endif

% if ('reviewer' in [x.name for x in c.signed_in_person.roles]) or ('organiser' in [x.name for x in c.signed_in_person.roles]):
<table>
<tr>
<th># - Reviewer</th>
<th>Score</th>
<th>Rec. Stream</th>
<th>Comment</th>
</tr>

%   for r in c.proposal.reviews:
<tr class="${ h.cycle('even', 'odd') }">
<td style="vertical-align: top;">
${ h.link_to("%s - %s" % (r.id, r.reviewer.firstname), url=h.url_for(controller='review', id=r.id, action='view')) }
</td>

<td style="vertical-align: top;">
${ r.score | h }
</td>

<td style="vertical-align: top;">
% if r.stream is not None:
${ r.stream.name | h }
% else:
(none)
% endif
</td>

<td style="vertical-align: top;">
${ h.line_break(h.util.html_escape(r.comment)) | n}
</td>

</tr>
%   endfor
</table>
% endif

## FIXME: wiki disabled
##<div id="wiki">
##${ h.wiki_here() }
##</div>

${ next.body() }


