	<p class="label"><label for="proposal.title">Title:</label><span class="mandatory">*</span><span class="publishable">&#8224;</span></p>
	<p class="entries"><% h.textfield('proposal.title', size=70) %></p>
		<p class="note">The name of your presentation.</p>

	<p class="label"><label>Type:</label><span class="mandatory">*</span><span class="publishable">&#8224;</span></p>
	<p class="entries">
% for st in c.cfptypes:
%   if st.name == 'Miniconf':
%     continue
%   # endif
    <label><% h.radio('proposal.type', st.id) %>
%   if st.name == 'Presentation':
      Presentation</label><br>
%   else:
      <% st.name |h %></label><br>
%   #endif
% #endfor
	</p>
		<p class="note" style="margin-top: 0em">The type of your
		presentation. If in doubt, choose "Presentation".</p>

	<p class="label"><label
	for="proposal.abstract">Abstract:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span></p>
	<p class="entries"><% h.textarea('proposal.abstract', size="70x10") %></p>
		<p class="note">This will appear in the conference
		programme. You will have an opportunity to update it once
		the presentation is accepted, but it should reasonably
		reflect what you will be presenting, and in any case it
		will appear as-is on the website in the draft programme. Up
		to about 500 words.</p>


	<p class="label"><label for="proposal.project">Project:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span>
	<p class="entries"><% h.textfield('proposal.project', size=70) %></p>
		<p class="note">The name of the project you will be talking
		about.</p>

	<p class="label"><label for="proposal.url">Project homepage:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span></p>
	<p class="entries"><% h.textfield('proposal.url', size=70) %></p>

		<p class="note">If your project has a webpage, specify the
		URL here so the committee can find out more about your
		proposal.</p>

	<p class="label"><label for="proposal.abstract_video_url">Video
	abstract:</label></p>
	<p class="entries"><% h.textfield('proposal.abstract_video_url', size=70) %></p>
		<p class="note">URL for a short "elevator pitch" (20s -
		3min) video about your presentation, your project or
		yourself (eg: YouTube link).</p>

	<p class="label"><label>Travel &amp; Accommodation
	Assistance:</label><span class="mandatory">*</span></p>
	<p class="entries">
% for ta in c.tatypes:
    <label><% h.radio('proposal.assistance', ta.id) %>
    <% ta.name |h %></label><br>
% #endfor
	</p>
		<p class="note" style="margin-top: 0em">Travel assistance
		is available to speakers who qualify. If you think you need
		it, please let us know. Please put any additional details
		into the "Personal experience" field, below.</p>

<h2>About yourself</h2>

<p><em>Note: These are common for all your proposals, both mini-confs and
presentations.</em></p>

<P>If two or more people are presenting together, this information should
for the primary speaker; mention the other speakers in the Abstract, eg.
"(with Bob Vaxhacker and Eve Duo)".</p>

% if c.signed_in_person:
%     c.person = c.signed_in_person
	<p class="label"><label
	for="name">Speaker name:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span></p>
	<p class="entries"><% h.textfield('name',
	value=c.person.firstname + " " + c.person.lastname, size=70,
	disabled=True) %></p>
		<p class="note">(Can't be changed here.)</p>

	<p class="label"><label
	for="person.url">Speaker mobile phone:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span></p>
	<p class="entries"><% h.text_field('person.url', size=70) %></p>
		<p class="note">Your mobile phone.</p>
% else:
c.mobile_is_mandatory = True
<& ../person/form.myt &>
% #endif

	<p class="label"><label
	for="person.url">Speaker homepage:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span></p>
	<p class="entries"><% h.textfield('person.url', size=70) %></p>
		<p class="note">Your homepage.</p>

	<p class="label"><label for="person.bio">Bio:</label><span class="mandatory">*</span><span
    class="publishable">&#8224;</span></p>
	<p class="entries"><% h.textarea('person.bio', size="70x6") %></p>
		<p class="note">This will appear on the conference website
		and in the programme for your talks and tutorials. Please
		write in the third person, eg "Alice is a Mozilla
		hacker...", 150-200 words.</p>

	<p class="label"><label for="person.experience">Relevant experience:</label></p>
	<p class="entries"><% h.textarea('person.experience', size="70x6") %></p>
		<p class="note">Have you had any experience presenting
		elsewhere? If so, we'd like to know. Anything you put here
		will only be seen by the organisers and reviewers; use it
		to convince them why they should accept your mini-confs and
		presentations.</p>

	<p>&nbsp;</p>
	<p class="note"><span class="mandatory">*</span> - Mandatory
	field</p>
	<p class="note"><span class="publishable">&#8224;</span> - Will be
	published (if your presentation is accepted)</p>

	<p class="note-bene">We reserve the right to forward submissions
	(accepted or not) to the miniconf organisers.</p>

