    <h2>Registration List</h2>
    <table> 
      <tr>
        <th>Rego</th>
        <th>Name</th>
        <th>Email</th>
        <th>Over 18</th>
        <th>Role</th>
        <th>Products</th>
        <th>Voucher</th>
        <th>Notes</th>
      </tr>
% for registration in c.registration_collection:
      <tr>
        <td><% h.link_to('id: ' + str(registration.id), url=h.url(action='view', id=registration.id)) %></td>
        <td><% h.link_to(m.apply_escapes(registration.person.firstname + ' ' + registration.person.lastname, 'h'), h.url(controller='person', action='view', id=registration.person.id)) %></td>
        <td><% registration.person.email_address | h %></td>
        <td><% h.yesno(registration.over18) %></td>
        <td>
%   role = []
%   if registration.person.is_speaker():
%       role.append('Speaker')
%   if registration.person.is_miniconf_org():
%       role.append('miniconf Organiser')
%   if registration.person.is_volunteer() == None:
%       role.append('Volunteer pending')
%   elif registration.person.is_volunteer() == True:
%       role.append('Volunteer')
%   #endif
%   for auth_role in registration.person.roles:
%       role.append(auth_role.name)
%   #endfor
        <% '<i>' + '</i>, <i>'.join(role) + '</i>' %>
        </td>
        <td>
%   for rproduct in registration.products:
          <% rproduct.qty %> x <% rproduct.product.description %><br>
%   #endfor
        </td>
        <td>
%   if registration.voucher:
%       for vproduct in registration.voucher.products:
          <% vproduct.qty %> x <% vproduct.product.description %> @ <% h.number_to_percentage(vproduct.percentage) %> Discount<br>
%       #endfor
%   #endif
        </td>
        <td>
            <% '<br><br>'.join(["<b>Note by <i>" + n.by.firstname + " " + n.by.lastname + "</i> at <i>" + n.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") + "</i>:</b><br>" + h.line_break(n.note) for n in registration.notes]) + '<br><br>' %>
%   if registration.diet:
            <% '<b>Diet:</b> %s<br><br>' % (registration.diet) %>
%   #endif
%   if registration.special:
            <% '<b>Special Needs:</b> %s<br><br>' % (registration.special) %>
%   #endif
        <% h.link_to("Add New Note", h.url(controller='rego_note', action='new', rego_id=registration.id)) %>
        </td>
      </tr>
% #endfor
    </table>
