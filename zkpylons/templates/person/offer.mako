<%inherit file="/base.mako" />
<h2 class="pop">Proposal Offers</h2>

%if c.person.proposals:
%  if c.person.proposal_offers:
<p>The following proposals that you submitted have been accepted by the ${ h.event_name() } proposal review committee:
${ h.form(h.url_for(), method='post') }
<table>
  <tr>
    <th>Title</th>
    <th>Abstract</th>
  </tr>
%    for offer in c.offers:
  <tr>
    <td>${ offer.title }</td>
    <td>${ h.line_break(h.util.html_escape(offer.abstract)) | n}</td>
  </tr>
%    endfor
</table>

<p>Please indicate below what you would like to do with these proposals:</p>
${ h.select('status', 'accept', [('accept', 'I accept these offers to present at ' + h.event_name()), ('withdraw', 'I withdraw my proposals'), ('contact', 'I require further contact with the conference organisers')]) }

<p>If you will be travelling to the conference from overseas please refer to the <a href="http://www.immi.gov.au/visitors/event-organisers-participants/participants.htm">Australian Immigration Department</a> website about the Visa requirements to visit Australia</p>

%if c.travel_assistance and c.accommodation_assistance:
<p>You have been offered Travel and Accommodation Assistance and we require some additional details from you so that we can book your travel:</p>
%elif c.accommodation_assistance:
<p>You have been offered Accommodation Assistance and further details of this will be provided to you closer to the event.</p>
%elif c.travel_assistance:
<p>You have been offered Travel Assistance and we require some additional details from you so that we can book your travel:</p>
%else
<p>You have not been offered any assistance to attend the conference.</p>
%endif

% if c.travel_assistance:
<label for="person.origin_airport">Source City or Airport Code:</label></p>
<p class="entries">${ h.text('travel.origin_airport') }</p>

<label for="person.destination_airport">Destination City or Airport Code:</label></p>
<p class="entries">${ h.text('travel.destination_airport') }</p>
%endif

<p class="submit">${ h.submit("submit", "Submit",) }</p>

${ h.end_form() }

%  else:
<p>No proposal offers outstanding</p>
%  endif
%else:
<p>No proposals submitted</p>
%endif
