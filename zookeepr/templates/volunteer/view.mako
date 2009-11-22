<%inherit file="/base.mako" />

<h2>Volunteer Details</h2>
% if c.volunteer.accepted:
    <p>Your application to be a volunteer has been accepted</p>
% endif
%  if h.auth.authorized(h.auth.has_organiser_role):
<table>
    <tr>
        <td><b>Name:</b></td>
        <td>${ h.link_to(c.volunteer.person.fullname(), url=h.url_for(controller='person', id=c.volunteer.person.id)) }</td>
    </tr>
    <tr>
        <td><b>Email:</b></td>
        <td><a href="mailto:${ c.volunteer.person.email_address }">${ c.volunteer.person.email_address }</a></td>
    </tr>
    <tr>
      <td><b>Speaker:</b></td>
      <td>
% if c.volunteer.person.is_speaker():
         Yes
% else:
         No
% endif
    </tr>
    <tr>
      <td><b>Miniconf Org:</b></td>
      <td>
% if c.volunteer.person.is_miniconf_org():
         Yes
% else:
         No
% endif
    </tr>
    <tr>
      <td valign="top"><b>Roles:</b></td>
      <td>
% if len(c.volunteer.person.roles) > 0:
<%  first = True %>
%   for role in c.volunteer.person.roles:
%     if first:
<%    first = False %>
%     else:
<br />
%     endif
<%
      if role.pretty_name is None or role.pretty_name == '':
        role_name = role.name 
      else:
        role_name = role.pretty_name 
%>
     ${ h.link_to(role_name, url=h.url_for(controller='role', action='view',id=role.id)) }
%    endfor
% else:
None
% endif
      </td>
    </tr>
% if c.volunteer.person.phone:
    <tr>
        <td><b>Phone:</b></td>
        <td>${ c.volunteer.person.phone }</td>
    </tr>
% endif
% if c.volunteer.person.mobile:
    <tr>
        <td><b>Mobile:</b></td>
        <td>${ c.volunteer.person.mobile }</td>
    </tr>
% endif
    <tr>
        <td><b>Country:</b></td>
        <td>${ c.volunteer.person.country }</td>
    </tr>
  </table>
% endif




    <p>These are the areas that have been chosen:</p>
    <table>
% for area in h.lca_rego['volunteer_areas']:
<% code = area['name'].replace(' ', '_').replace('.', '_') %>
      <tr class="${ h.cycle('even', 'odd') }">
        <td valign="middle" align="center">${ h.yesno(code in c.volunteer.areas) |n }</td>
        <td>${ area['name'] }
%   if area.has_key('description'):
          <p class="note"><small>${ area['description'] }</small></p>
%   endif
        </td>
      </tr>
% endfor
      <tr class="${ h.cycle('even', 'odd') }">
        <td>
          <p class="entries">Other:</p>
        </td>
        <td>
          <p class="entries"><blockquote>${ h.line_break(c.volunteer.other) }</blockquote></p>
          <p class="note"><small>Please provide any other relevant information such as your areas of interest, arrival and departure dates (if you're not local), your availability during LCA2010, and any special requirements (dietary or otherwise).</small></p>
        </td>
      </tr>

      <tr class="${ h.cycle('even', 'odd') }">
        <td>
          <p class="entries">Experience:</p>
        </td>
        <td>
          <p class="entries"><blockquote>${ h.line_break(c.volunteer.experience) }</blockquote></p>
          <p class="note"><small>Please provide details of your involvement at previous LCAs. If you have selected either of the technical options above (i.e., A/V or networking), then please indicate your relevant experience and skills here.</small></p>
        </td>
      </tr>
    </table>
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.volunteer.id)) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
