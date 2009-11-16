      <p>Please choose what areas you think you'll be able to help with at the conference</p>
      <table>
% for area in h.lca_rego['volunteer_areas']:
<% code = area['name'].replace(' ', '_').replace('.', '_') %>
        <tr class="${ h.cycle('even', 'odd') }">
          <td valign="middle" align="center">${ h.checkbox('volunteer.areas.' + code) }</td>
          <td>${ area['name'] }
%   if area.has_key('description'):
            <br><small>${ area['description'] }</small>
%   endif
          </td>
        </tr>
% endfor
        <tr class="${ h.cycle('even', 'odd') }">
          <td valign="top">
            <p class="entries">Other:</p>
          </td>
          <td>
            <p>${ h.textarea('volunteer.other', cols="60", rows="4") }</p>
            <p class="note">Please provide any other relevant information such as your areas of interest, arrival and departure dates (if you're not local), your availability during LCA2010, and any special requirements (dietary or otherwise).</p>
          </td>
        </tr>

        <tr class="${ h.cycle('even', 'odd') }">
          <td valign="top">
            <p class="entries">Experience:</p>
          </td>
          <td>
            <p>${ h.textarea('volunteer.experience', cols="60", rows="4") }</p>
            <p class="note">Please provide details of your involvement at previous LCAs. If you have selected either of the technical options above (i.e., A/V or networking), then please indicate your relevant experience and skills here.</p>
          </td>
        </tr>
      </table>
