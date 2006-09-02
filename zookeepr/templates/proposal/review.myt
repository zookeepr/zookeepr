<h1>Proposal Review</h2>

<% h.form(h.url_for()) %>

<h2><% c.proposal.title | h %></h2>

<fieldset>
<legend>Technical content</legend>

<p>
A proposal for a <% c.proposal.type.name %>.
</p>

<p>
Project URL:
% if c.proposal.url:
<% h.link_to(c.proposal.url, url=c.proposal.url) %>.
% else:
<em>none given</em>.
% #endif
</p>

<div class="data">
<% h.auto_link(h.simple_format(c.proposal.abstract)) %>
</div>

<div id="q1">
<p>1. How familiar are you with the subject matter of this talk?
<br />
<% h.radio_button('familiarity', 0) %>I don't know enough about the subject.
<br />
<% h.radio_button('familiarity', 1) %>I'm not an expert, but I feel comfortable with the subject matter.
<br />
<% h.radio_button('familiarity', 2) %>I'm an expert, I know the subject very well.
</p>
</div>

<div id="q2">
<p>2. "Proposal's technical quality, based on the abstract provided by the author."
</p>

<p>
% for i in range(1,6):
<% h.radio_button('technical', i) %>
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
<legend>Presenter's Experience/Bio</legend>

<div class="data">
<% h.auto_link(h.simple_format(c.proposal.experience)) %>
</div>

<div id="stalk">
<p>
Proposal submitted by:

<ul>
% for p in c.proposal.people:
<li>
<% h.link_to('Stalk %s on Google' % p.fullname, url='http://google.com/search?q=%s' % p.fullname) %>
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
<% h.radio_button('experience', i) %> <% i %>
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
<% h.radio_button('coolness', i) %> <% i %>
% #endfor
</p>
</div>

<div id="q5">
<p>
5. What stream do you think this talk is most suitable for?
</p>

<p>
<% h.select('stream', multiple=True, option_tags=h.options_for_select([['Free Love and Open Sexual Something', '19'],['Kernel Hax0ring', '18'],['Sysadmin/BOFH', '21'], ['Tools', '37']])) %>
</p>
</div>

<p>Comments (optional, readable by other reviewers, will not be shown to the submitter)

<% h.text_area('comments', size="80x10") %>
</p>

</fieldset>

<% h.submit('Submit review!') %>

<% h.end_form() %>

<%method title>
Review of <% h.truncate(c.proposal.title) %> - <& PARENT:title &>
</%method>
