% for st in c.proposal_types:
%    if st.name != 'Miniconf':
<%        continue %>
%    endif
<div>
<input type="hidden" name="proposal.type" value="${ st.id }" />
<input type="hidden" name="proposal.accommodation_assistance" value="1" />
<input type="hidden" name="proposal.travel_assistance" value="1" />
<input type="hidden" name="proposal.video_release" value="0" />
<input type="hidden" name="proposal.slides_release" value="0" />
<input type="hidden" name="proposal.abstract_video_url" value="" />
<input type="hidden" name="proposal.project" value="" />
</div>
% endfor

    <p class="label"><span class="mandatory">*</span><label for="proposal.title">Title:</label></p>
    <p class="entries">${ h.text('proposal.title', size=60) }</p>
    <p class="note">The name of your miniconf.</p>

    <p class="label"><span class="mandatory">*</span><label for="proposal.abstract">Miniconf summary:</label></p>
    <p class="entries">${ h.textarea('proposal.abstract', cols=70, rows=10) }</p>
    <p class="note">Please indicate any special requirements your miniconf may have (e.g. facilities required) and anticipated number of attendees, if possible.</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Target audience:</label></p>
    <p class="entries">
% for at in c.target_audiences:
    <label>${ h.radio('proposal.audience', at.id) }
    ${ at.name |h }</label><br>
% endfor
    </p>

    <p class="label"><label for="proposal.url">Miniconf URL:</label></p>
    <p class="entries">${ h.text('proposal.url', size=60) }</p>
    <p class="note">If your miniconf has a webpage, specify the URL here so the committee can find out more about your proposal.</p>

    <p class="label"><label for="attachment">Attach file:</label></p>
    <p class="entries">${ h.file('attachment', size=50) }</p>
    <p class="note">Any additional information, image, etc. You can attach and delete more files later by editing this proposal.</p>

    <h2>About yourself</h2>

    <p><em>Note: These are common for all your papers: miniconfs, presentations and tutorials.</em></p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="name">Organiser's name:</label></p>
    ${ h.hidden('person_to_edit', value=c.person.id) }
    <p class="entries">${ h.text('name', value=c.person.firstname + " " + c.person.lastname, size=60, disabled=True) }</p>
    <p class="note">(Can't be changed here.)</p>

    <p class="label"><span class="mandatory">*</span><label for="person.mobile">Organiser's mobile phone number:</label></p>
    <p class="entries">${ h.text('person.mobile', size=60) }</p>
    <p class="note">Your mobile phone number.</p>

    <p class="label"><span class="publishable">&#8224;</span><label for="person.url">Organiser's homepage:</label></p>
    <p class="entries">${ h.text('person.url', size=60) }</p>
    <p class="note">Your homepage.</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="person.bio">Biography:</label></p>
    <p class="entries">${ h.textarea('person.bio', cols=70, rows=6) }</p>
    <p class="note">Please write in the third person, eg "Alice is an Android hacker...", 150-200 words.</p>

    <p class="label"><span class="mandatory">*</span><label for="person.experience">Relevant experience:</label></p>
    <p class="entries">${ h.textarea('person.experience', cols=70, rows=6) }</p>
    <p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. Anything you put here will only be seen by the organisers and reviewers; use it to convince them why they should accept your miniconf.</p>

    <p>&nbsp;</p>
    <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
    <p class="note"><span class="publishable">&#8224;</span> - Will be published (if your presentation is accepted)</p>
