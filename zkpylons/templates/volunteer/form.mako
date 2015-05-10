      <p>${ c.config.get('event_shortname') } is a grass-roots conference and needs enthusiastic people like you to make it a success! This is a great opportunity to be seen by your peers and give back to the community.</p>

      <p>Volunteers will be expected to attend a training course which will walk them thru tasks such as operating cameras, registering people, etc. Training courses will be held in mid-December, mid-January, and on the weekend before the conference.</p>

      <p>Please use the check-boxes below to indicate your category, your availability, and areas that you are able to assist with. Please use the "Other:" and "Experience:" text boxes to let us know about any restrictions on your time or special skills you have that might help at the conference.</p>

      <table>
% for category in c.config.get('volunteer', category='rego'):
        <tr>
          <td colspan='2'><h3>${ category['title'] }</h3></td>
        </tr>
%   for area in category['questions']:
<%    code = area['name'].replace(' ', '_').replace('.', '_') %>
        <tr class="${ h.cycle('even', 'odd') }">
          <td valign="middle" align="center">${ h.checkbox('volunteer.areas.' + code) }</td>
          <td>${ area['name'] }
%     if area.has_key('description'):
            <br><small>${ area['description'] }</small>
%     endif
          </td>
        </tr>
%   endfor
% endfor
        <tr>
            <td colspan='2'><h3>Other Information</h3></td>
        </tr>
        <tr class="${ h.cycle('even', 'odd') }">
          <td valign="top">
            <p class="entries">Other:</p>
          </td>
          <td>
            <p>${ h.textarea('volunteer.other', cols="60", rows="4") }</p>
            <p class="note">Please provide any other relevant information such as your areas of interest, arrival and departure dates (if you're not local), your availability during ${ c.config.get('event_shortname') }, and any special requirements (dietary or otherwise).</p>
          </td>
        </tr>

        <tr class="${ h.cycle('even', 'odd') }">
          <td valign="top">
            <p class="entries">Experience:</p>
          </td>
          <td>
            <p>${ h.textarea('volunteer.experience', cols="60", rows="4") }</p>
            <p class="note">Please provide details of your involvement at previous conferences. If you have selected the technical option above (i.e., A/V), then please indicate your relevant experience and skills here.</p>
          </td>
        </tr>
      </table>
