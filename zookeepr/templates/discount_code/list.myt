<h2>Discount Codes</h2>

<table>.
    <tr>
        <th>Code</th>
        <th>Rego Type</th>
        <th>Percentage Discount</th>
        <th>Comment</th>
        <th>Used</th>
    </tr>

% for d in discount_codes:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><% d.code %></td>
        <td><% d.type %></td>
        <td><% d.percentage %></td>
        <td><% d.comment %></td>
%     if d.registrations:
        <td>True</td>
%     else:
        <td><strong>False</strong></td>
%     # endif
    </tr>
% #endfor

</table>
<%init>

discount_codes = c.discount_code_collection

</%init>


