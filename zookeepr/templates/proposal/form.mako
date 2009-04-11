    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="proposal.title">Title:</label></p>
    <p class="entries">${ h.text('proposal.title', size=70) }</p>
    <p class="note">The name of your presentation.</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Type:</label></p>
    <p class="entries">
% for st in c.proposal_types:
<%
   if st.name == 'Miniconf':
       continue
%>
    <label>${ h.radio('proposal.type', st.id) } ${ st.name |h }</label><br>
% endfor
    </p>
    <p class="note" style="margin-top: 0em">The type of your presentation. If in doubt, choose "Presentation".</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="proposal.abstract">Abstract:</label></p>
    <p class="entries">${ h.textarea('proposal.abstract', size="70x10") }</p>
    <p class="note">This will appear in the conference programme. You will have an opportunity to update it once the presentation is accepted, but it should reasonably reflect what you will be presenting, and in any case it will appear as-is on the website in the draft programme. Up to about 500 words.</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Target audience:</label></p>
    <p class="entries">
% for at in c.target_audiences:
    <label>${ h.radio('proposal.audience', at.id) }
    ${ at.name |h }</label><br>
% endfor
    </p>

    <p class="label"><span class="publishable">&#8224;</span><label for="proposal.project">Project:</label></p>
    <p class="entries">${ h.text('proposal.project', size=70) }</p>
    <p class="note">The name of the project you will be talking about.</p>

    <p class="label"><span class="publishable">&#8224;</span><label for="proposal.url">Project homepage:</label></p>
    <p class="entries">${ h.text('proposal.url', size=70) }</p>

    <p class="note">If your project has a webpage, specify the URL here so the committee can find out more about your proposal.</p>

    <p class="label"><label for="proposal.abstract_video_url">Video abstract:</label></p>
    <p class="entries">${ h.text('proposal.abstract_video_url', size=70) }</p>
    <p class="note">URL for a short "elevator pitch" (20s - 3min) video about your presentation, your project or yourself (eg: YouTube link).</p>
% if h.url_for().endswith('edit') is not True:
    <p class="label"><label for="attachment">Attach file:</label></p>
    <p class="entries">${ h.file('attachment', size=60) }</p>
    <p class="note">Any additional information, image, etc. You can attach and delete more files later by editing this proposal.</p>
% else:
    <p class="entries">${ h.link_to('Add an attachment', url=h.url_for(action='attach')) } ${ h.hidden('attachment', size=60) }<span class="note">You can attach multiple files by following this link.</span></p>
% endif
    <p class="label"><span class="mandatory">*</span><label>Travel &amp; Accommodation Assistance:</label></p>
    <p class="label"><label>Travel &amp; Accommodation Assistance:</label></p>
    <p class="note" style="margin-top: 0em">linux.conf.au has some funds available to provide travel and accommodation for selected speakers, both from the local region and internationally.</p>

    <p class="note" style="margin-top: 0em">Please note that <b>free admission</b> to the full conference is awarded to all primary presenters.</p>

    <p class="label"><span class="mandatory">*</span><label>Travel assistance:</label></p>
    <p class="entries">
<% onclick = "document.getElementById('travelwarning').style.display = 'none';" %>
% for ta in c.travel_assistance_types:
    <label><% h.radio('proposal.travel_assistance', ta.id, None, onclick) %>
    ${ ta.name |h }</label><br>
    <% onclick = "document.getElementById('travelwarning').style.display = '';" %>
% endfor
    </p>

    <p id="travelwarning" class="warningbox" style="display: none">WARNING: We have a limited travel budget and requesting travel assistance <b>affects     your chances of acceptance</b>.</p>

    <p class="label"><span class="mandatory">*</span><label>Accommodation assistance:</label></p>
    <p class="entries">
% for aa in c.accommodation_assistance_types::
    <label><% h.radio('proposal.accommodation_assistance', aa.id) %>
    ${ aa.name |h }</label><br>
% endfor
    </p>

    <h2>About yourself</h2>

    <p><em>Note: These are common for all your proposals, both mini-confs and presentations.</em></p>

    <p>If two or more people are presenting together, this information should for the primary speaker; mention the other speakers in the Abstract, eg. "(with Bob Vaxhacker and Eve Duo)".</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="name">Speaker name:</label></p>
    <p class="entries">${ h.text('name', value=c.person.firstname + " " + c.person.lastname, size=70,disabled=True) }</p>
    <p class="note">(Can't be changed here.)</p>

    <p class="label"><span class="mandatory">*</span><label for="person.mobile">Speaker mobile phone:</label></p>
    <p class="entries">${ h.text('person.mobile', size=70) }</p>
    <p class="note">Your mobile phone.</p>


    <p class="label"><span class="publishable">&#8224;</span><label for="person.url">Speaker homepage:</label></p>
    <p class="entries">${ h.text('person.url', size=70) }</p>
    <p class="note">Your homepage.</p>

    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="person.bio">Bio:</label></p>
    <p class="entries">${ h.textarea('person.bio', size="70x6") }</p>
    <p class="note">This will appear on the conference website and in the programme for your talks and tutorials. Please write in the third person, eg "Alice is a Mozilla hacker...", 150-200 words.</p>

    <p class="label"><span class="mandatory">*</span><label for="person.experience">Relevant experience:</label></p>
    <p class="entries">${ h.textarea('person.experience', size="70x6") }</p>
    <p class="note">Have you had any experience presenting elsewhere? If so, we'd like to know. Anything you put here will only be seen by the organisers and reviewers; use it to convince them why they should accept your mini-confs and presentations.</p>

    <p class="entries">
      ${ h.check_box('proposal.video_release') }
      <label for="proposal.video_release">I allow Linux Australia to
      release my video under the Creative Commons ShareAlike License</label>
    </p>

    <p class="entries">
      ${ h.check_box('proposal.slides_release') }
      <label for="proposal.slides_release">I allow Linux Australia to share my slides</label>
    </p>


    <p>&nbsp;</p>
    <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
    <p class="note"><span class="publishable">&#8224;</span> - Will be published (if your presentation is accepted)</p>

    <p>We reserve the right to forward submissions (accepted or not) to the miniconf organisers for possible inclusion in the miniconf programme.</p>
