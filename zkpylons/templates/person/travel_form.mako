%if c.travel_assistance:
<p>As you have been offered Travel Assistance we require some additional details from you:</p>

<label for="person.origin_airport">Source City or Airport:</label></p>
<p class="entries">${ h.text('travel.origin_airport') }</p>

<label for="person.destination_airport">Destination City or Airport:</label></p>
<p class="entries">${ h.text('travel.destination_airport') }</p>
%else:
${ h.hidden('travel.source_city', None) }
${ h.hidden('travel.destination_city', None) }
%endif
