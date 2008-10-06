    <h2>Registration List</h2>
    <table> 
      <tr>
        <th>Rego</th>
        <th>Name</th>
        <th>Email</th>
        <th>Over 18</th>
        <th>Speaker</th>
        <th>Products</th>
        <th>Voucher</th>
      </tr>
% for registration in c.registration_collection:
      <tr>
        <td><% h.link_to('id: ' + str(registration.id), url=h.url(action='view', id=registration.id)) %></td>
        <td><% h.link_to(m.apply_escapes(registration.person.firstname + ' ' + registration.person.lastname, 'h'), h.url(controller='person', action='view', id=registration.person.id)) %></td>
        <td><% registration.person.email_address | h %></td>
        <td><% h.yesno(registration.over18) %></td>
        <td><% h.yesno(registration.person.is_speaker()) %></td>
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
      </tr>
% #endfor
    </table>
