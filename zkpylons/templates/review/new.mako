<%namespace name="toolbox" file="/leftcol/toolbox.mako"/>
<%inherit file="/proposal/view_base.mako" />

<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
% if c.next_review_id:
  ${ toolbox.make_link('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }
% endif
</%def>

<%def name="heading()">
  Proposal Review - #${ c.proposal.id } - ${ c.proposal.title }
</%def>

% if c.next_review_id:
${ toolbox.make_link('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }
% else:
<ul><li><em>Can't skip - you have reviewed all the other ${c.proposal.type.name }s!</em></li></ul>
% endif

${ h.form(h.url_for()) }

<%include file="form.mako" />

<p class="submit">
${ h.submit('submit', 'Submit review and jump to next proposal!') }
</p>

<p>
% if c.next_review_id:
${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) } - 
% endif
${ h.link_to('Back to proposal list', url=h.url_for(controller='proposal', action='review_index')) }
</p>
${ h.end_form() }

<%def name="title()">
Reviewing proposal #${ c.proposal.id } - ${ parent.title() }
</%def>
