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
          <td colspan="2">
            <p class="entries">Other: ${ h.textarea('volunteer.other', cols="40", rows="4") }</p>
            <p class="note">Any other areas of interest or useful skills. Arrival and departure dates, if you're not local.</p>
          </td>
        </tr>
      </table>
