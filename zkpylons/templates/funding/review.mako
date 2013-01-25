<%inherit file="view_base.mako" />

<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
% if c.next_review_id:
  <li>${ h.link_to('Skip!', url=h.url_for(controller='funding', action='review', id=c.next_review_id)) }</li>
% endif
</%def>


<%def name="heading()">
  Funding Application Review - #${ c.funding.id } - ${ c.funding.person.fullname } - ${ c.funding.type.name }
</%def>

${ h.form(h.url_for()) }

% if c.next_review_id:
<ul><li>${ h.link_to('Skip!', url=h.url_for(controller='funding', action='review', id=c.next_review_id)) }</li></ul>
% else:
<ul><li><em>Can't skip - you have reviewed all the other ${c.funding.type.name }s!</em></li></ul>
% endif

<h3>Review</h3>
  <% reviewed_already = False %>
% for x in c.funding.reviews:
%   if x.reviewer == c.signed_in_person:
<p>You have already reviewered this funding. To modify your review, ${ h.link_to('click here', url=h.url_for(controller='funding_review', action='edit', id=x.id)) }.</p>
        <% reviewed_already = True %>
        <% break %>
%   endif
% endfor
% if not reviewed_already:
<fieldset>
<legend>
Your opinion on this funding application.
</legend>

<div id="q1">
<p class="label"><span class="mandatory">*</span><b>What score do you give this application?</b></p>
<p class="entries">
${ h.radio('review.score', 'null', label="Abstain") }
<br>
${ h.radio('review.score', '-2', label="-2 (strong reject) I want this funding application to be rejected, and if asked to I will advocate for it to be rejected.") }
<br>
${ h.radio('review.score', '-1', label="-1 (reject) I want this funding application to be rejected") }
<br>
${ h.radio('review.score', '+1', label="+1 (accept) I want this funding application to be accepted") }
<br>
${ h.radio('review.score', '+2', label="+2 (strong accept) I want this funding application to be accepted, and if asked to I will advocate for it to be accepted.") }
</p>
</div>

<p class="label"><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)
</p>
<p class="entries">
${ h.textarea('review.comment', cols="80", rows="10") }
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="submit">
${ h.submit('submit', 'Submit review and jump to next funding application!') }
</p>

% endif

<p>
% if c.next_review_id:
${ h.link_to('Skip!', url=h.url_for(controller='funding', action='review', id=c.next_review_id)) } - 
% endif
${ h.link_to('Back to funding list', url=h.url_for(controller='funding', action='review_index')) }
</p>
${ h.end_form() }

<%def name="title()">
Reviewing funding #${ c.funding.id } - ${ parent.title() }
</%def>
