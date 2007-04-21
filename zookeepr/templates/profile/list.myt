<h2> Profiles </h2>
<table> 
    <tr>
        <th>id</th>
        <th>Name</th>
        <th>Email</th>
    </tr>

% for p in c.profile_collection:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td class="list"><% h.link_to(p.id, url=h.url(controller='profile', action='view', id=p.id)) %></td>
        <td class="list"><% p.firstname %> <% p.lastname %></td>
        <td class="list"><% p.email_address %></td>
    </tr>
% #endfor
</table>
