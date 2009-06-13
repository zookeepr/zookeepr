<%inherit file="/base.mako" />

<h2>Volunteer Details</h2>
% if c.volunteer.accepted:
    <p>Your application to be a volunteer has been accepted</p>
% endif
    <p>These are the areas that have been chosen:</p>
    <table>
% for area in h.lca_rego['volunteer_areas']:
<% code = area['name'].replace(' ', '_').replace('.', '_') %>
      <tr class="${ h.cycle('even', 'odd') }">
        <td valign="middle" align="center">${ h.yesno(code in c.volunteer.areas) |n }</td>
        <td>${ area['name'] }
%   if area.has_key('description'):
          <br><small>${ area['description'] }</small>
%   endif
        </td>
      </tr>
% endfor
      <tr class="${ h.cycle('even', 'odd') }">
        <td colspan="2">
          <p class="entries">Other: ${ h.line_break(c.volunteer.other) }</p>
          <p class="note">Any other areas of interest or useful skills. Arrival and departure dates, if you're not local.</p>
        </td>
      </tr>
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.volunteer.id)) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
