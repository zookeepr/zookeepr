<h2>Volunteer Details</h2>
% if c.volunteer.accepted:
    <p>Your application to be a volunteer has been accepted</p>
% #endif
    <p>These are the areas that have been chosen:</p>
    <table>
% for area in h.lca_rego['volunteer_areas']:
% code = area['name'].replace(' ', '_').replace('.', '_')
      <tr class="<% oddeven() %>">
        <td valign="middle" align="center"><% h.yesno(code in c.volunteer.areas) %></td>
        <td><% area['name'] %>
%   if area.has_key('description'):
          <br><small><% area['description'] %></small>
%   #endif
        </td>
      </tr>
% #endfor
      <tr class="<% oddeven() %>">
        <td colspan="2">
          <p class="entries">Other: <% h.line_break(c.volunteer.other) %></p>
          <p class="note">Any other areas of interest or useful skills. Arrival and departure dates, if you're not local.</p>
        </td>
      </tr>
    </table>
    <p>
% if c.can_edit:
      <% h.link_to('Edit', url=h.url(action='edit',id=c.volunteer.id)) %> |
% #end if
      <% h.link_to('Back', url=h.url(action='index', id=None)) %>
    </p>
<%init>
def oddeven():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven().next
</%init>
