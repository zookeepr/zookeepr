<%inherit file="/base.mako" />
<h2 class="pop">Proposal Offers</h2>

%if c.person.proposals:
%  if c.person.proposal_offers:
<p>The following proposals that you have submitted has been accepted by the ${ h.event_name() } proposal review committee:
${ h.form(h.url_for(), method='post') }
<table>
  <tr>
    <th>Title</th>
    <th>Abstract</th>
    <th>Travel Assistance</th>
    <th>Accomodation Assistance</th>
  </tr>
%    for offer in c.offers:
  <tr>
    <td>${ offer.title }</td>
    <td>${ h.line_break(h.util.html_escape(offer.abstract)) | n}</td>
    <td>${ offer.travel_assistance.name }</td>
    <td>${ offer.accommodation_assistance.name }</td>
  </tr>
%    endfor
</table>

<p>Please indicate below what you would like to do with these proposals:</p>
${ h.select('status', 'accept', [('accept', 'I accept these offers to present at ' + h.event_name()), ('withdraw', 'I withdraw my proposals'), ('contact', 'I require further contact with the conference organisers')]) }

<%include file='travel_form.mako' />

<p class="submit">${ h.submit("submit", "Submit",) }</p>

${ h.end_form() }

%  else:
<p>No proposal offers outstanding</p>
%  endif
%else:
<p>No proposals submitted</p>
%endif
