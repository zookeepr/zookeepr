<tr>
	<td></td>
	<td><span class="mandatory">*</span> - Mandatory field</td>
</tr>

<tr>
	<th class="labels"><span class="mandatory">*</span><label for="person.experience">Experience:</label></th>
	<td class="entries"><% h.text_area('person.experience', size="50x10") %>
		<p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. 
			Anything you put here will only be seen by the reviewers; 
			Use it to convince them why they should accept your paper.</p>
	</td>
</tr>

<tr>
	<th class="labels"><span class="mandatory">*</span><label for="person.bio">Bio:</label></th>
	<td class="entries"><% h.text_area('person.bio', size="50x10") %>
		<p class="note">Your Bio, this will appear on the conference website.</p>
	</td>
</tr>

<tr>
	<td colspan="2"><p>Tell us a bit about the proposal you'd like to submit:</p></td>
</tr>
	
<tr>
	<th class="labels"><span class="mandatory">*</span><label for="proposal.title">Title:</label></th>
	<td class="entries"><% h.text_field('proposal.title', size=50) %>
		<p class="note">e.g. the name of your talk, tutorial or miniconf.</p>
	</td>
</tr>

<tr>
	<th class="labels"><span class="mandatory">*</span>Type:</th>
	<td class="entries">

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
	<p class="note">What sort of proposal is this?</p>
	</td>
</tr>

<tr>
	<th class="labels"><label for="proposal.url">Project URL:</label></th>
	<td class="entries"><% h.text_field('proposal.url', size=50) %>
		<p class="note">If your proposal has a project URL, specify it here so the review committee can find out more about your proposal.</p>
	</td>
</tr>

<tr>
	<th class="labels"><label for="attachment">Attach paper:</label></th>
	<td class="entries"><% h.file_field('attachment', size=50) %>
		<p class="note">If you are submitting a paper, please upload it here.</p>
	</td>
</tr>

<tr>
	<th class="labels"><span class="mandatory">*</span><label for="proposal.abstract">Proposal Abstract:</label></th>
	<td class="entries"><% h.text_area('proposal.abstract', size="50x20") %>
		<p class="note">Please write here a summary of your proposal.  Your proposal will be judged on the description you provide.</p>
	</td>
</tr>

<tr>
	<th class="labels"><span class="mandatory">*</span><label>Travel &amp; Accommodation Assistance:</label></th>
	<td class="entries">
% for ta in c.tatypes:
    <% h.radio_button('proposal.assistance', ta.id) %>&nbsp;<label for="proposal.assistance"><% ta.name |h %></label><br />

% #endfor
	<p class="note">Travel assistance is available to speakers who qualify.  If you think you need it, please let us know.</p>
	</td>
</tr>