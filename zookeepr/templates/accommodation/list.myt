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
<% h.number_to_currency(a.cost_per_night) %>
</td>

<td>
<% a.beds |h %>
</td>

<td>
<% a.get_available_beds() |h %>
</td>

</tr>

% #endfor

</table>

<%method title>
Accommodation - <& PARENT:title &>
</%method>
