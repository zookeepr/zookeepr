<%page args="editing" />

  <fieldset id="personal">
    <legend>&nbsp;</legend>
    <h2>Funding Programme</h2>

    <p class="label"><span class="mandatory">*</span><label>What funding programme are you applying for?</label></p>
    <p class="entries">
% for st in c.funding_types:
%  if st.available():
      <label>${ h.radio('funding.type', st.id) } ${ st.name }</label><br>
%  endif
% endfor
    </p>
    <p class="note">Please select the Funding Programme you are applying for.</p>
  </fieldset>

  <fieldset id="google">
    <legend>&nbsp;</legend>
    <h2>Information for Google Diversity Programme</h2>

    <p class="label"><label for="funding.male">What gender are you?</label></p>
    <p class="entries">
       <label>${ h.radio('funding.male', 0) } Female</label><br />
       <label>${ h.radio('funding.male', 1) } Male</label><br />
    </p>

    <p class="label"><label for="funding.diverse_groups">If applicable, what minority group(s) within the Open Source community do you belong to?</label></p>
    <p class="entries">${ h.textarea('funding.diverse_groups', cols=70, rows=10) }</p>
    <p class="note">Please indicate what minority group you belong to (for example, be female, or have a disability) and how being a member of this minority group makes you diverse to the Open Source Community.</p>
  </fieldset>

  <fieldset id="prev_info">
    <legend>&nbsp;</legend>
    <h2>${ h.event_name() } Information</h2>

    <p class="label"><label for="funding.prevlca">Have you attended linux.conf.au before?</label></p>
    <p class="entries">
    <table>
      <tr>
        <td>
% for (year, desc) in h.lca_rego['past_confs']:
         <% label = 'funding.prevlca.%s' % year %>
<label>${ h.checkbox(label) } ${ desc }</label><br />
% endfor
        </td>
      </tr>
    </table>
    </p>

    <p class="label"><span class="mandatory">*</span><label for="funding.why_attend">Why would you like to attend ${ h.event_name() }?</label></p>
    <p class="entries">${ h.textarea('funding.why_attend', cols=70, rows=10) }</p>
    <p class="note">Please describe why you would like to attend ${ h.event_name() } and indicate the talks that particularly interest you. Up to about 500 words.</p>
  </fieldset>

  <fieldset id="info">
    <legend>&nbsp;</legend>
    <h2>Funding Information</h2>


    <p class="label"><span class="mandatory">*</span><label for="funding.how_contribute">How do you contribute to the Open Source community?</label></p>
    <p class="entries">${ h.textarea('funding.how_contribute', cols=70, rows=10) }</p>
    <p class="note">Please describe in what way you contribute to the open source community (for example, as a developer, documentor, QA/testing, bug submitter, Open Source advocate/community champion, or other leadership roles).  Up to about 500 words.</p>

    <p class="label"><span class="mandatory">*</span><label for="funding.financial_circumstance">What are your financial circumstances?</label></p>
    <p class="entries">${ h.textarea('funding.financial_circumstances', cols=70, rows=10) }</p>
    <p class="note">Please describe the financial circumstances that are stopping you from otherwise attending ${ h.event_name() }.</p>

    <p class="label"><label for="funding.supporting_information">Any other supporting information?</label></p>
    <p class="entries">${ h.textarea('funding.supporting_information', cols=70, rows=10) }</p>
    <p class="note">Please provide any additional information that may assist your application.</p>
  </fieldset>

  <fieldset id="references">
    <legend>&nbsp;</legend>
    <h2>References</h2>

% if not editing:
    <p class="label"><label for="attachment1">First Character Reference:</label></p>
    <p class="entries">${ h.file('attachment1', size=50) }</p>
    <p class="note">Please upload your first character reference (friend, colleague or employer in the Open Source Community).</p>

    <p class="label"><label for="attachment2">Second Character Reference:</label></p>
    <p class="entries">${ h.file('attachment2', size=50) }</p>
    <p class="note">Please upload your second character reference (friend, colleague or employer in the Open Source Community).</p>
% else:
    <p class="entries">${ h.link_to('Add an attachment', url=h.url_for(action='attach')) } ${ h.hidden('attachment', size=60) }<span class="note">You can attach multiple files by following this link.</span></p>
% endif
  </fieldset>


