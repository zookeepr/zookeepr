<%page args="editing" />
<div>
<input type="hidden" name="proposal.type" />
<input type="hidden" name="proposal.technical_requirements" value="" />
<input type="hidden" name="proposal.accommodation_assistance" value="1" />
<input type="hidden" name="proposal.travel_assistance" value="1" />
<input type="hidden" name="proposal.video_release" value="0" />
<input type="hidden" name="proposal.slides_release" value="0" />
<input type="hidden" name="proposal.abstract_video_url" value="" />
<input type="hidden" name="proposal.project" value="" />
</div>

    <div class="row form-group">
      <label for="proposaltitle" class="col-sm-2 control-label">Title</label>
      <div class="input-group">
        <input type="text" id="proposaltitle" class="form-control" placeholder="The name of your miniconf." name="proposal.title" required/>
        <span class="glyphicon form-control-feedback" ></span>
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>

    <div class="row form-group"> 
      <div class="textarea">
        <label for="proposalabstract" class="col-sm-2 control-label">Miniconf summary</label>
        <div class="input-group col-sm-10">
            <textarea class="form-control" id="proposalabstract" placeholder="This will appear in the conference programme. You will have an opportunity to update it once the proposal is accepted, but it should reasonably reflect what your miniconf is about, and in any case it will appear as-is on the website in the draft programme." name="proposal.abstract" rows="10" cols="80" required></textarea>
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
      </div>
    </div>

    <div class="row form-group"> 
      <div class="textarea">
        <label for="proposalpriveate_abstract" class="col-sm-2 control-label">Private summary</label>
        <div class="input-group col-sm-10">
            <textarea class="form-control" id="proposalprivate_abstract" placeholder="This will only be shown to organisers and reviewers. You should provide any details about your miniconf that you don't want to be public here. Please indicate any special requirements your miniconf may have (e.g. facilities required) and anticipated number of attendees, if possible." name="proposal.private_abstract" rows="10" cols="80" required></textarea>
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
      </div>
    </div>

    <div class="row form-group">
      <label for="proposalaudience" class="col-sm-2 control-label">Target audience</label>
          <div class="col-sm-10">
% for at in c.target_audiences:
            <div class="input-group radio">
              <label>
                <input type="radio" name="proposal.audience" id="proposal.audience_${ at.id }" value="${ at.id }">
                ${ at.name }
              </label>
            </div>
% endfor
          </div>
    </div>

    <div class="row form-group">
      <label for="proposalurl" class="col-sm-2 control-label">Miniconf URL:</label>
      <div class="col-sm-10">
        <input type="text" id="proposalurl" class="form-control" placeholder="A webpage where the committee can find out more about your proposal. (Optional)" name="proposal.url" />
      </div>
    </div>

    <div class="row form-group">
      <label for="attachment" class="col-sm-2 control-label">Attachments</label>
      <div class="col-sm-10">
% if not editing:
        <input type="file" id="attachment" name="attachment">
        <p class="help-block">Any additional information, image, etc. You can attach and delete more files later by editing this submission.</p>
% else:
% if len(c.proposal.attachments) > 0:
    <table class="table sortable">
      <tr>
        <th>Filename</th>
        <th>Size</th>
        <th>Date uploaded</th>
        <th>&nbsp;</th>
      </tr>
% for a in c.proposal.attachments:
      <tr>
        <td> ${ h.link_to(h.util.html_escape(a.filename), url=h.url_for(controller='attachment', action='view', id=a.id)) }</td>
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
        <td>  ${ h.link_to('delete', url=h.url_for(controller='attachment', action='delete', id=a.id)) } </td>
      <tr>
% endfor
    </table>
% endif
    <a class="btn btn-default" href="./attach">Attach multiple files</a>
    <p class="help-block">Making changes to attachments from this screen will force you to leave this form. Either open the attachment links in a new tab, or complete the changes <b>after</b> submitting this form.</p>
% endif
      </div>
    </div>

<!-- About the speaker -->
    <h2>About yourself</h2>

    <p class="lead"><em>Note: These settings are common for all your proposals, miniconfs, presentations and tutorials.</em></p>


    <div class="row form-group"> 
      <label for="person.name" class="col-sm-2 control-label">Organisers name</label>
      <input id="person_to_edit" name="person_to_edit" type="hidden" value="1">
      <div class="input-group col-sm-10">
        <input class="form-control" disabled="disabled" id="personname" readonly name="person.name" required></input>
        <span class="input-group-addon" id="basic-addon2">See user profile</span>
      </div>
    </div>
    
 <!--   
    <p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label for="person.name">Organiser's name:</label></p>
    ${ h.hidden('person_to_edit', value=c.person.id) }
    <p class="entries">${ h.text('person.name', size=60, disabled=True) }</p>
    <p class="note">(Can't be changed here.)</p>
    -->

    <div class="row form-group"> 
      <label for="name" class="col-sm-2 control-label">Organisers phone</label>
      <div class="input-group col-sm-10">
       <div class="input-group">
        <input class="form-control" id="personphone" name="person.phone" required></input>
        <span class="input-group-addon" id="basic-addon2">required</span>
       </div>
      <p class="help-block">The conference team will need this to contact you during the conference week. If you don't have one, or do not wish to provide it, then enter NONE in this field</p>
      </div>
    </div>
    
    <div class="row form-group"> 
      <label for="personurl" class="col-sm-2 control-label">Organiser's homepage</label>
      <div class="input-group col-sm-10">
        <input type="text" class="form-control" id="personurl" name="person.url" placeholder="www" ></input>
      </div>
    </div>
    
    <div class="row form-group"> 
      <div class="textarea">
        <label for="personbio" class="col-sm-2 control-label">Biography</label>
        <div class="input-group col-sm-10">
            <textarea class="form-control" id="personbio" placeholder="Please write in the third person, eg Alice is a KVM hacker..., 150-200 words." name="person.bio" rows="10" cols="80" required></textarea>
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
      </div>
    </div>

    <div class="row form-group"> 
      <div class="textarea">
        <label for="personexperience" class="col-sm-2 control-label">Relevant Experience</label>
        <div class="input-group col-sm-10">
            <textarea class="form-control" id="personexperience" placeholder="Have you had any experience presenting elsewhere? If so, we'd like to know. Anything you put here will only be seen by the organisers and reviewers; use it to convince them why they should accept your miniconf." name="person.experience" rows="10" cols="80" required></textarea>
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
      </div>
    </div>
