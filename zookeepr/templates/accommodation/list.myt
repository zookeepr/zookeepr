<h1>Accommodation</h1>

<table>

<th>#</th>

<th>Location</th>

<th>Option</th>

<th>Cost per night</th>

<th>Capacity (# beds)</th>

<th>Availability (# beds left)</th>

% for a in c.accommodation_collection:

<tr class="<% h.cycle('even', 'odd')%>">

<td>
<% a.id %>
</td>

<td>
<% a.name %>
</td>

<td>
<% a.option %>
</td>

<td>
<% a.cost_per_night %>
</td>

<td>
<% a.beds %>
</td>

<td>
<% a.get_available_beds() %>
</td>

</tr>

% #endfor

</table>

<%method title>
Accommodation - <& PARENT:title &>
</%method>
