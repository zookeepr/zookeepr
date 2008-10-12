      <p>Please choose what areas you think you'll be able to help with at the conference</p>
      <table>
% for area in h.lca_rego['volunteer_areas']:
%   code = area['name'].replace(' ', '_').replace('.', '_')
        <tr class="<% oddeven() %>">
          <td valign="middle" align="center"><% h.check_box('volunteer.areas.' + code) %></td>
          <td><% area['name'] %>
%   if area.has_key('description'):
            <br><small><% area['description'] %></small>
%   #endif
          </td>
        </tr>
% #endfor
        <tr class="<% oddeven() %>">
          <td colspan="2">
            <p class="entries">Other: <% h.text_area('volunteer.other', size='40x4') %></p>
            <p class="note">Any other areas of interest or useful skills. Arrival and departure dates, if you're not local.</p>
          </td>
        </tr>
      </table>
<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven().next
</%init>
