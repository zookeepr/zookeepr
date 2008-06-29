% for st in c.cfptypes:
%    if st.name != 'Miniconf':
%        continue
%    # endif
<div><% h.hiddenfield('proposal.type', st.id) %>
<% h.hiddenfield('proposal.assistance', 0) %></div>

% #endfor

    <p class="label"><span class="mandatory">*</span><label for="proposal.title">Title:</label></p>
    <p class="entries"><% h.textfield('proposal.title', size=70) %></p>
    <p class="note">The name of your miniconf.</p>

    <p class="label"><span class="mandatory">*</span><label for="proposal.abstract">Mini-conf summary:</label></p>
    <p class="entries"><% h.textarea('proposal.abstract', size="70x10") %></p>
    <p class="note-bene">Please indicate any special needs your miniconf will have (e.g. facilities required), preferred duration (1 day / 2 days) and anticipated number of attendees, if possible.</p>

    <p class="label"><label for="proposal.url">Miniconf URL:</label></p>
    <p class="entries"><% h.textfield('proposal.url', size=70) %></p>
    <p class="note">If your miniconf has a webpage, specify the URL here so the committee can find out more about your proposal.</p>

    <p class="label"><label for="attachment">Attach file:</label></p>
    <p class="entries"><% h.file_field('attachment', size=60) %></p>
    <p class="note">Any additional information, image, etc. You can attach and delete more files later by editing this proposal.</p>

    <h2>About yourself</h2>

    <p><em>Note: These are common for all your proposals, both mini-confs and presentations.</em></p>

% if c.signed_in_person:
%     c.person = c.signed_in_person
    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="name">Organiser name:</label></p>
    <p class="entries"><% h.textfield('name', value=c.person.firstname + " " + c.person.lastname, size=70, disabled=True) %></p>
    <p class="note">(Can't be changed here.)</p>

    <p class="label"><span class="mandatory">*</span><label for="person.mobile">Organiser mobile phone:</label></p>
    <p class="entries"><% h.textfield('person.mobile', size=70) %></p>
    <p class="note">Your mobile phone.</p>

% else:
%   c.mobile_is_mandatory = True
<& ../person/form.myt &>
% #endif

    <p class="label"><span class="publishable">&#8224;</span><label for="person.url">Organiser homepage:</label></p>
    <p class="entries"><% h.textfield('person.url', size=70) %></p>
    <p class="note">Your homepage.</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="person.bio">Bio:</label></p>
    <p class="entries"><% h.textarea('person.bio', size="70x6") %></p>
    <p class="note">This will appear on the conference website and in the programme for your talks and tutorials. Please write in the third person, eg "Alice is a Mozilla hacker...", 150-200 words.</p>

    <p class="label"><span class="mandatory">*</span><label for="person.experience">Relevant experience:</label></p>
    <p class="entries"><% h.textarea('person.experience', size="70x6") %></p>
    <p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. Anything you put here will only be seen by the organisers and reviewers; use it to convince them why they should accept your mini-confs and presentations.</p>

    <p>&nbsp;</p>
    <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
    <p class="note"><span class="publishable">&#8224;</span> - Will be published (if your presentation is accepted)</p>
