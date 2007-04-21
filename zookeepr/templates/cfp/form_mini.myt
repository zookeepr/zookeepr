% for st in c.cfptypes:
%    if st.name != 'Miniconf':
%        continue
%    # endif

    <% h.hidden_field('proposal.type', st.id) %>

% #endfor

<tr>
	<td><span class="mandatory">*</span> - Mandatory field</td>
</tr>

<tr>
	<th class="label"><span class="mandatory">*</span><label for="person.experience">Experience:</label></th>
</tr>
<tr>
	<td class="entries"><% h.text_area('person.experience', size="50x10") %>
		<p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. 
			Anything you put here will only be seen by the
			reviewers; Use it to convince them why they should
			accept your mini-confs and papers.</p>
	</td>
</tr>

<tr>
	<th class="label"><span class="mandatory">*</span><label for="person.bio">Bio:</label></th>
</tr>
<tr>
	<td class="entries"><% h.text_area('person.bio', size="50x10") %>
		<p class="note">Your Bio, this will appear on the conference website.</p>
	</td>
</tr>

<tr>
	<td colspan="2"><p>Tell us a bit about the mini-conf you'd like to run:</p></td>
</tr>
	
<tr>
	<th class="label"><span class="mandatory">*</span><label for="proposal.title">Title:</label></th>
</tr>
<tr>
	<td class="entries"><% h.text_field('proposal.title', size=50) %>
		<p class="note">The name of your miniconf.</p>
	</td>

<tr>
	<th class="label"><label for="proposal.url">Project URL:</label></th>
</tr>
<tr>
	<td class="entries"><% h.text_field('proposal.url', size=50) %>
		<p class="note">If your proposal has a project URL, specify it here so the review committee can find out more about your proposal.</p>
	</td>
</tr>

<tr>
	<th class="label"><label for="attachment">Attach paper:</label></th>
</tr>
<tr>
	<td class="entries"><% h.file_field('attachment', size=50) %>
		<p class="note">If you are submitting a paper, please upload it here.</p>
	</td>
</tr>

<tr>
	<th class="label"><span class="mandatory">*</span><label for="proposal.abstract">Proposal Abstract:</label></th>
</tr>
<tr>
	<td class="entries"><% h.text_area('proposal.abstract', size="50x20") %>
		<p class="note">Please write here a summary of your proposal. 
		Please indicate any special requirements your miniconf will
		have (any special needs or facilities required), preferred
		duration (1 day / 2 days) and anticipated number of attendees,
		if possible.</p>
	</td>
</tr>

<tr>
	<th class="label"><span class="mandatory">*</span><label>Travel &amp; Accommodation Assistance:</label></th>
</tr>
<tr>
	<td class="entries">
% for ta in c.tatypes:
    <% h.radio_button('proposal.assistance', ta.id) %>&nbsp;<label for="proposal.assistance"><% ta.name |h %></label><br />

% #endfor
	<p class="note">Travel assistance is available to speakers who qualify.  If you think you need it, please let us know.</p>
	</td>
</tr>
