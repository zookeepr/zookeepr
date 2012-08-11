<%namespace name="toolbox" file="/leftcol/toolbox.mako"/>
<%inherit file="/base.mako" />
<% c.signed_in_person = h.signed_in_person() %>
<%def name="toolbox_extra()">
% if h.auth.authorized(h.auth.has_organiser_role) or ((c.proposal_editing == 'open' or h.auth.authorized(h.auth.has_late_submitter_role)) and c.signed_in_person in c.proposal.people):
  ${ toolbox.make_link('Edit Proposal', url=h.url_for(controller='proposal', action='edit', id=c.proposal.id)) }
% endif 
</%def>

<%def name="toolbox_extra_reviewer()">
## Add review link if the signed in person is a reviewer, but not if they've already reviewed this proposal
% if h.url_for().endswith('review') is not True and h.url_for().endswith('edit') is not True:
  ${ toolbox.make_link('Review this proposal', url=h.url_for(action='review')) }
% endif
</%def>

<%def name="heading()">
  ${ c.proposal.title }
</%def>

<% c.signed_in_person = h.signed_in_person() %>

<h2>${ self.heading() }</h2>


% if c.proposal.type.name == 'Miniconf':
  <%include file="view_fragment_miniconf.mako" />
% else:
  <%include file="view_fragment.mako" />
% endif

% if h.auth.authorized(h.auth.has_organiser_role) or ((c.proposal_editing == 'open' or h.auth.authorized(h.auth.has_late_submitter_role)) and c.signed_in_person in c.proposal.people):
${ toolbox.make_link('Edit Proposal', url=h.url_for(controller='proposal', action='edit',id=c.proposal.id)) }
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
%if len(c.streams) > 1:
<th>Rec. Stream</th>
%endif
<th>Comment</th>
<th>Private Comment</th>
</tr>

%   for r in c.proposal.reviews:
<tr class="${ h.cycle('even', 'odd') }">
<td style="vertical-align: top;">
${ h.link_to("%s - %s %s" % (r.id, r.reviewer.firstname, r.reviewer.lastname), url=h.url_for(controller='review', id=r.id, action='view')) }
</td>

<td style="vertical-align: top;">
${ r.score | h }
</td>

%if len(c.streams) > 1:
<td style="vertical-align: top;">
% if r.stream is not None:
${ r.stream.name | h }
% else:
(none)
% endif
</td>
%endif

<td style="vertical-align: top;">
${ h.line_break(h.util.html_escape(r.comment)) | n}
</td>

<td style="vertical-align: top;">
${ h.line_break(h.util.html_escape(r.private_comment)) | n}
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


