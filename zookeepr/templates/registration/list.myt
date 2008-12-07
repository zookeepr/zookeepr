<script type="text/javascript">
function display_toggle(box)
{
    div = document.getElementById(box);
    if (div.style['display'] == 'none')
    {
        div.style['display'] = 'block';
    }
    else
    {
        div.style['display'] = 'none';
    }
    return false;
}
</script>

    <h2>Registration List</h2>
    <table> 
      <thead><tr>
        <th>Rego</th>
        <th>Name</th>
        <th>Email</th>
        <th>Role(s)</th>
        <th>Invoices</th>
        <th>Notes</th>
      </tr></thead>
% for registration in c.registration_collection:
      <tr>
        <td><% h.link_to('id: ' + str(registration.id), url=h.url(action='view', id=registration.id)) %></td>
        <td><% h.link_to(m.apply_escapes(registration.person.firstname + ' ' + registration.person.lastname, 'h'), h.url(controller='person', action='view', id=registration.person.id)) %></td>
        <td><% registration.person.email_address | h %></td>
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
%   for rinvoice in registration.person.invoices:
        <% h.link_to(rinvoice.id, h.url(controller='invoice', action='view', id=rinvoice.id)) %> - <small><% rinvoice.status() %></small>
%       if rinvoice.manual is True:
            <i>(manual)</i>
%       #endif
        <small><a href="#" onclick="return display_toggle('products_<% rinvoice.id %>')">+</a></small>
%       display = "display: none;"
%       if rinvoice.void is not True: display=""
        <div id="products_<% rinvoice.id %>" style="<% display %> background: #ddd;">
%       for rproduct in rinvoice.items:
          <% rproduct.qty %><small> x <% rproduct.description %></small><br>
%       #endfor
        </div>
%   #endfor
%   if registration.voucher:
        <i>Voucher Used:</i>
%       for vproduct in registration.voucher.products:
          <% vproduct.qty %><small> x <% vproduct.product.description %> @ <% h.number_to_percentage(vproduct.percentage) %> Discount</small><br>
%       #endfor
%   #endif
        </td>
        <td>
%   if not registration.over18:
        <b>Under 18</b> <% h.yesno(not registration.over18) %><br><br>
%   #endif
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
