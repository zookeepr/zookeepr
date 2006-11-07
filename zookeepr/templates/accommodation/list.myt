<h1>Acoommodation</h1>

<table>

% for a in c.accommodation_collection:

<tr>

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
beds left
</td>

</tr>

% #endfor

</table>
