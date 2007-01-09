<h2>Discount Codes</h2>

<table>.
    <tr>
        <th>Code</th>
        <th>Rego Type</th>
        <th>Percentage Discount</th>
        <th>Comment</th>
        <th>Used By</th>
    </tr>

% for d in discount_codes:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><% d.code %></td>
        <td><% d.type %></td>
        <td><% d.percentage %></td>
        <td><% d.comment %></td>
%     if d.registrations:
        <td><% d.registrations[0].person.firstname + " " + d.registrations[0].person.lastname %>
%          if d.registrations[0].company:
                <% "(" + d.registrations[0].company + ")"%>
%          # endif
</td>
%     else:
        <td><strong>Hasn't been used</strong></td>
%     # endif
    </tr>
% #endfor

</table>
<br />
 <% h.link_to('(Add another)', url=h.url(controller='discount_code', action='new')) %>

<%init>

discount_codes = c.discount_code_collection

</%init>


