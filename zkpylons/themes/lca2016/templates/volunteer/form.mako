        <p>linux.conf.au is a grass-roots conference and needs enthusiastic people like you to make it a success! This is a great opportunity to be seen by your peers and give back to the open source community.</p>
        <p>As a volunteer, you will be expected to attend a training course which will walk you through tasks such as operating cameras, registering people, etc. Training courses will be held in mid-January, and on the weekend before the conference.</p>
        <p>Please use the check-boxes below to indicate your category, your availability, and areas that you are able to assist with. Please use the "Other:" and "Experience:" text boxes to let us know about any restrictions on your time or special skills you have that might help at the conference.</p>
        <p>We thank you in advance for your enthusiasm and commitment to making linux.conf.au 2016 Geelong - LCA By the Bay - the best LCA ever!</p>

% for category in c.config.get('volunteer', category='rego'):
        <h3>${ category['title'] }</h3>
%   for area in category['questions']:
<%    code = area['name'].replace(' ', '_').replace('.', '_') %>
        <div class="form-group">
          <div class="checkbox">
            <label>
              <input type="checkbox" value="" id="${'volunteerareas' + code}" name="${'volunteer.areas.' + code}">
              ${ area['name'] }
%     if area.has_key('description'):
              <span id="helpBlock" class="help-block">${ area['description'] }</span>
%     endif
            </label>
          </div>
        </div>
%   endfor
% endfor
        <h3>Other Information</h3>
        <div class="row form-group"> 
          <div class="textarea">
            <label for="volunteer.other" class="col-sm-2 control-label">Other</label>
            <div class="input-group col-sm-10">
              <textarea class="form-control" id="proposalabstract" placeholder="Please provide any other relevant information such as your areas of interest, arrival and departure dates (if you're not local), your availability during ${ c.config.get('event_shortname') }, and any special requirements (dietary or otherwise)." name="volunteer.other" rows="10" cols="80"></textarea>
            </div>
          </div>
        </div>
        <div class="row form-group"> 
          <div class="textarea">
            <label for="volunteer.experience" class="col-sm-2 control-label">Experience</label>
            <div class="input-group col-sm-10">
              <textarea class="form-control" id="volunteer.experience" placeholder="Please provide details of your involvement at previous conferences. If you have selected the technical option above (i.e., A/V), then please indicate your relevant experience and skills here." name="volunteer.experience" rows="10" cols="80"></textarea>
            </div>
          </div>
        </div>
