<h1>Proposal Review</h2>

<% h.form(h.url_for()) %>

<h2><% c.proposal.title | h %></h2>

<fieldset>
<legend>Proposal's technical content</legend>

<p>
This is a proposal for a <% c.proposal.type.name %>.
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

<div id="q1">
<p>1. How familiar are you with the subject matter of this talk?
<br />
<% h.radio_button('review.familiarity', 0) %>I don't know enough about the subject.
<br />
<% h.radio_button('review.familiarity', 1) %>I'm not an expert, but I feel comfortable with the subject matter.
<br />
<% h.radio_button('review.familiarity', 2) %>I'm an expert, I know the subject very well.
</p>
</div>

<div id="q2">
<p>2. "Proposal's technical quality, based on the abstract provided by the author."
</p>

<p>
% for i in range(1,6):
<% h.radio_button('review.technical', i) %>
%	if i == 0:
NA
%	else:
<% i %>
%	#endif
% #endfor
</p>
</div>

</fieldset>

<fieldset>
<legend>Presenter's experience/biography</legend>

<blockquote>
<% h.auto_link(h.simple_format(c.proposal.experience)) %>
</blockquote>

<div id="stalk">
<p>
Proposal submitted by:

<ul>
% for p in c.proposal.people:
<li>
<% p.fullname | h %> &lt;<% p.email_address %>&gt;
<% h.link_to('(stalk on Google)', url='http://google.com/search?q=%s+%s' % (p.fullname, p.email_address)) %>
<% h.link_to('(linux specific stalk)', url='http://google.com/linux?q=%s+%s' % (p.fullname, p.email_address)) %>
<% h.link_to('(email address only stalk)', url='http://google.com/search?q=%s' % p.email_address) %>
</li>
% #endfor
</ul>
</p>
</div>

<div id="q3">
<p>3. "Author's experience on the proposal's subject, based on the mini-curriculum provided by she/he and others sources (web searches, another events, performance among community etc)."
</p>

<p>
% for i in range(1,6):
<% h.radio_button('review.experience', i) %> <% i %>
% #endfor
</p>
#<br/>
</div>

</fieldset>

<fieldset>
<legend>
Summary
</legend>

<div id="q4">
<p>4. How excited are you to have this submission presented at linux.conf.au 2007?
</p>

<p>
% for i in range(1,6):
<% h.radio_button('review.coolness', i) %> <% i %>
% #endfor
</p>
</div>

<div id="q5">
<p>
5. What stream do you think this talk is most suitable for?
</p>

<p>
<% h.select('review.stream', option_tags=h.options_for_select_from_objects(c.streams, 'name', 'id')) %>
</p>
</div>

<p>Comments (optional, readable by other reviewers, will not be shown to the submitter)

<% h.text_area('review.comments', size="80x10") %>
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<% h.submit('Submit review!') %>

<% h.end_form() %>

<%method title>
Review of <% h.truncate(c.proposal.title) %> - <& PARENT:title &>
</%method>
