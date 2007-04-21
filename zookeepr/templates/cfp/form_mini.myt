% for st in c.cfptypes:
%    if st.name != 'Miniconf':
%        continue
%    # endif
<% h.hidden_field('proposal.type', st.id) %>

<% h.hidden_field('proposal.assistance', 0) %>

% #endfor

	<p><span class="mandatory">*</span> - Mandatory field</p>

	<p class="label"><span class="mandatory">*</span><label for="person.experience">Experience:</label></p>
	<p class="entries"><% h.text_area('person.experience', size="50x10") %></p>
 		<p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. 
			Anything you put here will only be seen by the
			organisers and reviewers; Use it to convince them why
			they should accept your mini-confs and papers.</p>

	<p class="label"><span class="mandatory">*</span><label for="person.bio">Bio:</label></p>
	<p class="entries"><% h.text_area('person.bio', size="50x10") %>
		<p class="note">Your Bio, this will appear on the conference website for your papers.</p>

	<h2>About the mini-conf</h2>

	<p class="label"><span class="mandatory">*</span><label for="proposal.title">Title:</label></p>
	<p class="entries"><% h.text_field('proposal.title', size=50) %></p>
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
	<th class="label"><span class="mandatory">*</span><label for="proposal.abstract">Mini-conf summary:</label></th>
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

