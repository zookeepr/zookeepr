<table>
  <tr>
    <th><label for="person.origin_airport">Origin</label></th>
    <th>&nbsp;</th>
    <th><label for="person.destination_airport">Destination</label></th>
  </tr>
  <tr>
    <td>${ h.text('travel.origin_airport') }</td>
    <td style="text-align: center;" >&rarr; ${ h.lca_info['event_airport_code'] } &rarr;</td>
    <td>${ h.text('travel.destination_airport') }</td>
  </tr>
</table
<p class='note'>Please supply Airport Codes or Cities for the Origin and Destination of your travel. We will fund one return airfare for you to attend ${ h.lca_info['event_name']}. If you want to be returned to the same airport, please enter the same details for both Origin and Destination.</p>
