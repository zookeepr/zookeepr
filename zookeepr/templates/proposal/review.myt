<h1>Proposal Review</h1>

<h2>#<% c.proposal.id %> - "<% c.proposal.title | h %>"</h2>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for()) %>

<fieldset>
<legend>Proposal's technical content</legend>

<p>
This is a proposal for a <strong><% c.proposal.type.name %></strong>
submitted at
<% c.proposal.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
(last updated at <% c.proposal.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>)
</p>

<p>
Project URL:
% if c.proposal.url:
<% h.link_to(c.proposal.url, url=c.proposal.url) %>.
% else:
<em>none given</em>.
% #endif
</p>

<p>Abstract:</p>
<blockquote>
<% h.auto_link(h.simple_format(c.proposal.abstract)) %>
</blockquote>

</fieldset>
<fieldset>
<legend>Presenter's experience/biography</legend>
% for person in c.proposal.people:
<h2><% person.firstname %> <% person.lastname %></h2>
<strong>Experience</strong>
<blockquote>
<% h.auto_link(h.simple_format(person.experience)) %>
</blockquote>
<strong>Bio</strong>
<blockquote>
<% h.auto_link(h.simple_format(person.bio)) %>
</blockquote>

<div id="stalk">
<p>
Proposal submitted by:

<ul>
<li>
<% person.firstname | h %> <% person.lastname | h %>&lt;<% person.email_address %>&gt;
<% h.link_to('(stalk on Google)', url='http://google.com/search?q=%s+%s' % (person.firstname + " " + person.lastname, person.email_address)) %>
<% h.link_to('(linux specific stalk)', url='http://google.com/linux?q=%s+%s' % (person.firstname + " " + person.lastname, person.email_address)) %>
<% h.link_to('(email address only stalk)', url='http://google.com/search?q=%s' % person.email_address) %>
</li>
</ul>
</p>
</div>

% #endfor
</fieldset>


<fieldset>
<div id="q1">
<p>1. What score do you give this paper?
<br />
<% h.radio('review.score', -2, "-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") %>
<br />
<% h.radio('review.score', -1, "-1 (reject) I want this proposal to be rejected") %>
<br />
<% h.radio('review.score', 0, "0 (indifferent) This proposal has no particular faults but no particular strengths") %>
<br />
<% h.radio('review.score', +1, "+1 (accept) I want this proposal to be accepted") %>
<br />
<% h.radio('review.score', +2, "+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") %>
</p>
</div>

<div id="q2">
<p>
2. What stream do you think this talk is most suitable for?
</p>

<p>
<% h.select('review.stream', option_tags=h.options_for_select_from_objects(c.streams, 'name', 'id')) %>
</p>
</div>

<p>3. Comments (optional, readable by other reviewers, will not be shown to the submitter)

<% h.text_area('review.comment', size="80x10") %>
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<% h.submit('Submit review and jump to next proposal!') %>

<% h.end_form() %>

</&>

<%method title>
Reviewing proposal #<% c.proposal.id %>, "<% h.truncate(c.proposal.title) %>" - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>
