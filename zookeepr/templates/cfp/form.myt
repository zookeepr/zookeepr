<h2>Submit a Proposal to the CFP</h2>

<div style="width: 600px; margin: auto;">

<fieldset>

<p>Tell us a bit about the proposal you'd like to submit:</p>

<p>
<span class="mandatory">*</span>
<label for="proposal.title">Title:</label>
<% h.text_field('proposal.title', size=50) %>
<br />
<span class="fielddesc">e.g. the name of your talk, tutorial or miniconf.</span>
</p>

<p>
<span class="mandatory">*</span>
<label>Type:</label>
<br />
% for st in c.cfptypes:
%    if c.cfp_mode == 'miniconf':
%        if st.name != 'Miniconf':
%           continue
%        # endif
%    else:
%        if st.name == 'Miniconf':
%           continue
%        # endif
%    # endif

    <% h.radio_button('proposal.type', st.id) %>
    <label for="proposal.type"><% st.name |h %></label><br />

% #endfor
<span class="fielddesc">What sort of proposal is this?</span>
</p>

<p><label for="proposal.url">Project URL:</label>
<% h.text_field('proposal.url', size=50) %>
<br />
<span class="fielddesc">If your proposal has a project URL, specify it here so the review committee can find out more about your proposal.</span>
</p>

<p><label for="attachment">Attach paper:</label>
<% h.file_field('attachment', size=50) %>
<br />
<span class="fielddesc">If you are submitting a paper for peer review, please upload it here.</span>
</p>

<p>
<span class="mandatory">*</span>
<label for="proposal.abstract">Proposal Abstract:</label>
<br />
<span class="fielddesc">Please write here a summary of your proposal.  Your proposal will be judged on the description you provide.</span>
<br />
<% h.text_area('proposal.abstract', size="50x20") %>
</p>

<p>
<span class="mandatory">*</span>
<label for="proposal.experience">Experience:</label>
<br />
<span class="fielddesc">Have you had any experience presenting elsewhere?  If so, we'd like to know.</span>
<br />
<% h.text_area('proposal.experience', size="50x10") %>
</p>

<p><label>Need travel assistance?</label>
<% h.check_box('proposal.assistance') %>
<br />
<span class="fielddesc">Travel assistance is available to speakers who qualify.  If you think you need it, please let us know.</span>
</p>

</fieldset>

</div>
