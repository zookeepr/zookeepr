<%page args="editing" />
    <div class="row form-group">
      <label for="fundingtype" class="col-sm-2 control-label">What funding programme are you applying for?</label>
      <div class="col-sm-10">
% for st in c.funding_types:
%  if st.available():
      <label>
        <input type="radio" name="funding.type" id="funding.type_${ st.id }" value="${ st.id }">
        ${ st.name }
      </label>
%  endif
% endfor
      </div>
    </div>

    <div class="row form-group">
      <label for="fundingdiverse_groups" class="control-label">In what way to you enhance the diversity of the Open Source community?</label>
      <div class="input-group">
        <textarea class="form-control" id="fundingdiverse_groups" placeholder="Please indicate how you enhance the diversity of the Open Source Community." name="funding.diverse_groups" rows="10" cols="80"></textarea>
      </div>
    </div>

    <div class="row form-group">
      <label for="fundinghow_contribue" class="control-label">How do you contribute to the Open Source community?</label>
      <div class="input-group">
        <textarea class="form-control" id="fundinghow_contribute" placeholder="Please describe in what way you contribute to the open source community (for example, as a developer, documenter, QA/testing, bug submitter, Open Source advocate/community champion, or other leadership roles). Up to about 500 words." name="funding.how_contribute" rows="10" cols="80"></textarea>
      </div>
    </div>

    <div class="row form-group">
      <label for="fundingfinancial_circumstances" class="control-label">What assistance would you need to be able to attend the conference?</label>
      <div class="input-group">
        <textarea class="form-control" id="fundingfinancial_circumstances" placeholder="Please describe the financial circumstances that prevent you from otherwise attending linux.conf.au 2016." name="funding.financial_circumstances" rows="10" cols="80"></textarea>
      </div>
    </div>

    <div class="row form-group">
      <label for="fundingsupporting_information" class="control-label">Any other supporting information?</label>
      <div class="input-group">
        <textarea class="form-control" id="fundingsupporting_information" placeholder="Please provide any additional information that may assist your application." name="funding.supporting_information" rows="10" cols="80"></textarea>
      </div>
    </div>

    <div class="row form-group">
      <label for="fundingwhy_attend" class="control-label">Why would you like to attend linux.conf.au 2016?</label>
      <div class="input-group">
        <textarea class="form-control" id="fundingwhy_attend" placeholder="Please describe why you would like to attend linux.conf.au 2016 and indicate the talks that particularly interest you. Up to about 500 words." name="funding.why_attend" rows="10" cols="80"></textarea>
      </div>
    </div>

    <div class=row form-group">
      <label for="fundingprevlca" class="control-label">Have you attended linux.conf.au before?</label>
      <div class="input-group">
%     for (year, desc) in h.lca_rego['past_confs']:
        <div class="checkbox">
          <label>
            <% label1 = 'registration.prevlca.%s' % year %>
            <% label2 = 'registrationprevlca%s' % year %>
            <input type="checkbox" name="${ label1 }" id="${ label2 }" value="1">
            ${ desc }
          </label>
        </div>
%     endfor
    </div>

    <h2>References</h2>

    <div class="row form-group">
      <label for="attachment1" class="col-sm-2 control-label">Attachments</label>
      <div class="col-sm-10">
% if not editing:
        <input type="file" id="attachment1" name="attachment1">
        <p class="help-block">Any additional information, image, etc. You can attach and delete more files later by editing this submission.</p>
% else:
% if len(c.funding.attachments) > 0:
    <table class="table sortable">
      <tr>
        <th>Filename</th>
        <th>Size</th>
        <th>Date uploaded</th>
        <th>&nbsp;</th>
      </tr>
% for a in c.funding.attachments:
      <tr>
        <td> ${ h.link_to(h.util.html_escape(a.filename), url=h.url_for(controller='funding_attachment', action='view', id=a.id)) }</td>
        <td>
%if len(a.content) >= (1024*1024):
${ round(len(a.content)/1024.0/1024.0, 1) } MB
%elif len(a.content) >= (1024):
${ round(len(a.content)/1024.0, 1) } kB
%else:
${ len(a.content) } B
%endif
        </td>
        <td>  ${ a.creation_timestamp.strftime("%Y-%m-%d %H:%M") } </td>
        <td>  ${ h.link_to('delete', url=h.url_for(controller='funding_attachment', action='delete', id=a.id)) } </td>
      <tr>
% endfor
    </table>
% endif
    <a class="btn btn-default" href="./attach">Attach multiple files</a>
    <p class="help-block">Making changes to attachments from this screen will force you to leave this form. Either open the attachment links in a new tab, or complete the changes <b>after</b> submitting this form.</p>
% endif
      </div>
    </div>
