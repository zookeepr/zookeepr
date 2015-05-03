<%page args="editing" />
    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="proposal.title">Title:</label></p>
    <p class="note">The name of your proposal.</p>
    <p class="entries">${ h.text('proposal.title', size=60) }</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Type:</label></p>
    <p class="note" style="margin-top: 0em">The type of your proposal. If in doubt, choose "Presentation".</p>
    <p class="entries">
% for st in c.proposal_types:
<%
   if st.name == 'Miniconf':
       continue
%>
    <label>${ h.radio('proposal.type', st.id) } ${ st.name |h }</label><br>
% endfor
    </p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="proposal.abstract">Abstract:</label></p>
    <p class="note">This will appear in the conference programme. You will have an opportunity to update it once the proposal is accepted, but it should reasonably reflect what you will be presenting, and in any case it will appear as-is on the website in the draft programme. Up to about 500 words.</p>
    <p class="entries">${ h.textarea('proposal.abstract', cols=70, rows=10) }</p>

    <p class="label"><label for="proposal.private_abstract">Private Abstract:</label></p>
    <p class="note">This will only be shown to organisers and reviewers. You should provide any details about your proposal that you don't want to be public here.</p>
    <p class="entries">${ h.textarea('proposal.private_abstract', cols=70, rows=10) }</p>

    <p class="label"><label for="proposal.technical_requirements">Non-standard technical requirements:</label></p>
    <p class="note">Speakers will be provided with: Internet access, power, projector, audio.  If you require anything in addition, please list your technical requirements here.  Such as: a static IP address, A/V equipment or will be demonstrating security-related techniques on the conference network.</p>
    <p class="entries">${ h.textarea('proposal.technical_requirements', cols=70, rows=3) }</p>


    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Target audience:</label></p>
    <p class="entries">
% for at in c.target_audiences:
    <label>${ h.radio('proposal.audience', at.id) }
    ${ at.name |h }</label><br>
% endfor
    </p>

    <p class="label"><span class="publishable">&#8224;</span><label for="proposal.project">Project:</label></p>
    <p class="note">The name of the project you will be talking about.</p>
    <p class="entries">${ h.text('proposal.project', size=60) }</p>

    <p class="label"><span class="publishable">&#8224;</span><label for="proposal.url">Project homepage:</label></p>
    <p class="note">If your project has a webpage, specify the URL here so the committee can find out more about your proposal.</p>
    <p class="entries">${ h.text('proposal.url', size=60) }</p>


    <p class="label"><label for="proposal.abstract_video_url">Video abstract:</label></p>
    <p class="note">URL for a short "elevator pitch" (20s - 3min) video about your proposal, your project or yourself (eg: YouTube link).</p>
    <p class="entries">${ h.text('proposal.abstract_video_url', size=60) }</p>

% if not editing:
    <p class="label"><label for="attachment">Attach file:</label></p>
    <p class="note">Any additional information, image, etc. You can attach and delete more files later by editing this submission.</p>
    <p class="entries">${ h.file('attachment', size=50) }</p>
% else:
    <p class="entries">${ h.link_to('Add an attachment', url=h.url_for(action='attach')) } ${ h.hidden('attachment', size=60) }<span class="note">You can attach multiple files by following this link.</span></p>
% endif

% if c.config.get('cfp_hide_assistance_options') is 'no':
    <h2>Travel &amp; Accommodation Assistance</h2>
    <p class="note" style="margin-top: 0em">linux.conf.au has some funds available to provide travel and accommodation for selected speakers, both from the local region and internationally.</p>

    <p class="note" style="margin-top: 0em">Please note that <b>free admission</b> to the full conference is awarded to all primary speakers.</p>

    <p class="label"><span class="mandatory">*</span><label>Travel assistance:</label></p>
    <p class="entries">
<% onclick = "document.getElementById('travelwarning').style.display = 'none';" %>
% for ta in c.travel_assistance_types:
    <label>${ h.radio('proposal.travel_assistance', ta.id, None,
    onclick=onclick) }
    ${ ta.name |h }</label><br>
    <% onclick = "document.getElementById('travelwarning').style.display = '';" %>
% endfor
    </p>

    <p id="travelwarning" class="warningbox" style="display: none">WARNING: We have a limited travel budget and requesting travel assistance <b>affects     your chances of acceptance</b>.</p>

    <p class="label"><span class="mandatory">*</span><label>Accommodation assistance:</label></p>
    <p class="entries">
% for aa in c.accommodation_assistance_types:
    <label>${ h.radio('proposal.accommodation_assistance', aa.id) }
    ${ aa.name |h }</label><br>
% endfor
    </p>
% else:
    ${ h.hidden('proposal.travel_assistance') }
    ${ h.hidden('proposal.accommodation_assistance') }
% endif

% if c.config.get('cfp_hide_assistance_options') is 'by_email': 
    <h2>Travel &amp; Accommodation Assistance</h2>
    <p class="note" style="margin-top: 0em">Please note that <b>free admission</b> to the full conference is offered to all speakers.</p>
    <p class="note" style="margin-top: 0em">Travel &amp; accommodation assistance <em>may</em> be available in circumstances where it is absolutely necessary. To find out more please e-mail <em>${ c.config.get('contact_email') }</em>.</p>
% endif


    <h2>About yourself</h2>

    <p><em>Note: These are common for all your proposals: presentations and tutorials.</em></p>

    <p>If two or more people are presenting together, this information should for the primary speaker; mention the other speakers in the Abstract, eg. "(with Bob Vaxhacker and Eve Duo)".</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="person.name">Speaker's name:</label></p>
    ${ h.hidden(name="person_to_edit", value="replaced by htmlfill.render(...)") }
    <p class="note">(Can't be changed here.)</p>
    <p class="entries">${ h.text('name', value="replaced by htmlfill.render(...)", size=60, disabled=True) }</p>

    <p class="label"><span class="mandatory">*</span><label for="person.mobile">Speaker's mobile phone:</label></p>
    <p class="note">The conference team will need this to contact you during the conference week. If you don't have one, or do not wish to provide it, then enter NONE in this field</p>
    <p class="entries">${ h.text('person.mobile', size=60) }</p>

    <p class="label"><span class="publishable">&#8224;</span><label for="person.url">Speaker's homepage:</label></p>
    <p class="note">Your homepage.</p>
    <p class="entries">${ h.text('person.url', size=60) }</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="person.bio">Biography:</label></p>
    <p class="note">This will appear on the conference website and in the programme.  Please write in the third person, eg "Alice is a Moblin hacker...", 150-200 words.</p>
    <p class="entries">${ h.textarea('person.bio', cols="70", rows="6") }</p>

    <p class="label"><span class="mandatory">*</span><label for="person.experience">Relevant experience:</label></p>
    <p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. Anything you put here will only be seen by the organisers and reviewers; use it to convince them why they should accept your proposal.</p>
    <p class="entries">${ h.textarea('person.experience', cols="70", rows="6") }</p>

    <p class="entries">
      ${ h.checkbox('proposal.video_release') }
      <label for="proposal.video_release">I allow ${ c.config.get("event_parent_organisation") } to
      release any recordings of my presentations, tutorials and minconfs under the <a href="${ c.config.get("media_license_url") }">${ c.config.get("media_license_name") }</a></label>
    </p>

    <p class="entries">
      ${ h.checkbox('proposal.slides_release') }
      <label for="proposal.slides_release">I allow ${ c.config.get("event_parent_organisation") } to release any other material (such as slides) from my presentations, tutorials and minconfs under the <a href="${ c.config.get("media_license_url") }">${ c.config.get("media_license_name") }</a></label>
    </p>


    <p>&nbsp;</p>
    <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
    <p class="note"><span class="publishable">&#8224;</span> - Will be published (if your proposal is accepted)</p>

    <p>We reserve the right to forward proposals (accepted or not) to the miniconf organisers for possible inclusion in the miniconf programme.</p>
