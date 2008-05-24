% for st in c.cfptypes:
%    if st.name != 'Miniconf':
%        continue
%    # endif
<% h.hidden_field('proposal.type', st.id) %>

<% h.hidden_field('proposal.assistance', 0) %>

% #endfor
	<br><p class="note"><span class="mandatory">*</span> - Mandatory
	field</p>

	<p class="label"><span class="mandatory">*</span><label for="proposal.title">Title:</label></p>
	<p class="entries"><% h.text_field('proposal.title', size=70) %></p>
		<p class="note">The name of your miniconf.</p>

	<p class="label"><span class="mandatory">*</span><label for="proposal.abstract">Mini-conf summary:</label></p>
	<p class="entries"><% h.text_area('proposal.abstract', size="70x10") %></p>
		<p class="note-bene">Please indicate any special needs your
		miniconf will have (e.g. facilities required), preferred
		duration (1 day / 2 days) and anticipated number of attendees,
		if possible.</p>

	<p class="label"><label for="proposal.url">Miniconf URL:</label></p>
	<p class="entries"><% h.text_field('proposal.url', size=70) %></p>
		<p class="note">If your miniconf has webpage, specify the URL here so the committee can find out more about your proposal.</p>

	<p class="label"><label for="attachment">Attach file:</label></th>
	<p class="entries"><% h.file_field('attachment', size=60) %></p>
		<p class="note">Any additional information, image, etc.</p>

<h2>About yourself</h2>

<p><em>Note: These are common for all your proposals, both mini-confs and
presentations.</em></p>

% if c.signed_in_person_id:
	<p class="label"><span class="mandatory">*</span><span
	class="publishable">&#8224;</span><label
	for="name">Organiser name:</label></p>
	<p class="entries"><% h.text_field('name',
	value=c.person.firstname + " " + c.person.lastname, size=70,
	disabled=True) %></p>
		<p class="note">(Can't be changed here.)</p>
% else:
<& ../person/form.myt &>
% #endif

	<p class="label"><span class="mandatory">*</span><span
	class="publishable">&#8224;</span><label
	for="person.url">Organiser homepage:</label></p>
	<p class="entries"><% h.text_field('person.url', size=70) %></p>
		<p class="note">Your homepage.</p>

	<p class="label"><span class="mandatory">*</span><label for="person.experience">Relevant experience:</label></p>
	<p class="entries"><% h.text_area('person.experience', size="70x6") %></p>
		<p class="note">Have you had any experience presenting
		elsewhere? If so, we'd like to know.  Anything you put here
		will only be seen by the organisers and reviewers; Use it to
		convince them why they should accept your mini-confs and
		presentations.</p>

	<p class="label"><span class="mandatory">*</span><label for="person.bio">Bio:</label></p>
	<p class="entries"><% h.text_area('person.bio', size="70x6") %></p>
		<p class="note">Your Bio, this will appear on the
		conference website for your presentations.</p>
