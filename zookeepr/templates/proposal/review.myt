<h1>Proposal Review</h2>

<% h.form(h.url_for()) %>

<p>review for</p>

<h2><% c.proposal.title | h %></h2>

<fieldset>
<legend>Abstract</legend>

<div class="data">
<% h.auto_link(h.simple_format(c.proposal.abstract)) %>
</div>

<p>How familiar are you with the subject matter of this talk?
<br />
<% h.radio_button('familiarity', 0) %>I don't know enough about the subject.
<br />
<% h.radio_button('familiarity', 1) %>I'm not an expert, but I feel comfortable with the subject matter.
<br />
<% h.radio_button('familiarity', 2) %>I'm an expert, I know the subject very well.
</p>

<p>"Proposal's technical quality, based on the abstract provided by the author."

% for i in range(1,6):
<% h.radio_button('technical', i) %>
%	if i == 0:
NA
%	else:
<% i %>
%	#endif
% #endfor
</p>

</fieldset>

<fieldset>
<legend>Experience/Bio</legend>

<div class="data">
<% h.auto_link(h.simple_format(c.proposal.experience)) %>
</div>

<p>"Author's experience on the proposal's subject, based on the mini-curriculum provided by she/he and others sources (web searches, another events, performance among community etc)."

% for i in range(1,6):
<% h.radio_button('experience', i) %> <% i %>
% #endfor
<br/>

*** support multiple people ***
<% h.link_to('google stalk this person', url='http://google.com/search?q=Lindsay%20Holmwood') %>
</p>

</fieldset>

<fieldset>
<legend>
Summary
</legend>

<p>How excited are you to have this submission presented at linux.conf.au 2007?

% for i in range(1,6):
<% h.radio_button('coolness', i) %> <% i %>
% #endfor
</p>

<p>
What stream do you think this talk is most suitable for?
</p>

<p>
<% h.select('stream', multiple=True, option_tags=h.options_for_select([['Free Love and Open Sexual Something', '19'],['Kernel Hax0ring', '18'],['Sysadmin/BOFH', '21'], ['Tools', '37']])) %>
</p>

<p>Comments (optional, readable by other reviewers, will not be shown to the submitter)

<% h.text_area('comments', size="80x10") %>
</p>

</fieldset>

<% h.submit('Submit review!') %>

<% h.end_form() %>
