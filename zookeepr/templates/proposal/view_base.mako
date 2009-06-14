<%inherit file="/base.mako" />
<%namespace file="reviewer_sidebar.mako" name="sidebar" inheritable="True"/>
<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
  <% c.signed_in_person = h.signed_in_person() %>
%   if c.signed_in_person in c.proposal.people or ('organiser' in [x.name for x in c.signed_in_person.roles]):
  <li>${ h.link_to('Edit Proposal', url=h.url_for(controller='proposal', action='edit',id=c.proposal.id)) }</li>

  ## Add review link if the signed in person is a reviewer, but not if they've already reviewed this proposal
%     if 'reviewer' in [x.name for x in c.signed_in_person.roles]:
%       if h.url_for().endswith('review') is not True and h.url_for().endswith('edit') is not True:
  <li>${ h.link_to('Review this proposal', url=h.url_for(action='review')) }</li>
%       endif
    ${ self.sidebar.toolbox_extra() }
%     endif
%   endif
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
${ r.stream.name | h }
</td>

<td style="vertical-align: top;">
${ h.line_break(r.comment) }
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


