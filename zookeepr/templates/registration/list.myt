<h1> Registration Report </h1>


<h2> Total Registrations </h2>

% if rego_total > 0:

<table> 
    <tr>
        <th>Type</th>
        <th>Num (Inc Speakers)</th>
        <th>Numr (Ex Speakers)</th>
        <th>Num Paid</th>
        <th>Percentage Paid</th>
        <th>Attendees Breakdown</th>
    </tr>
%   for type in rego_all:
    <tr class="<% h.cycle('even', 'odd')%> ">
        <td><% type %></td>
        <td><% rego_all[type] %></td>
        <td><% rego_nonspeaker.get(type, '-') %></td>
        <td><% rego_paid.get(type, '-') %></td>
%     if rego_total_nonspeaker > 0:
        <td><% h.number_to_percentage(rego_paid.get(type,0)*100/rego_total_nonspeaker, precision=0) %></td>
        <td><% h.number_to_percentage(rego_nonspeaker.get(type,0)*100/rego_total_nonspeaker, precision=0) %></td>
%     else:
        <td>-</td><td>-</td>
%     #endif
    </tr>
%   #endfor

<tr>
    <td><strong>Total</strong></td>
    <td><strong><% rego_total %></strong></td>
    <td><strong><% rego_total_nonspeaker %></strong></td>
    <td><strong><% rego_total_paid %></strong></td>
%   if rego_total_nonspeaker > 0:
    <td><strong><% h.number_to_percentage(rego_total_paid*100/rego_total_nonspeaker, precision=0) %></strong></td>
%   else:
    <td>-</td>
%   #endif
    <td><strong><% h.number_to_percentage(100, precision=0) %></strong></td>
</tr>

</table>

<strong>Extra Dinner Tickets: </strong><% extra_dinners %><br>
<!-- (seven calculation, ours is different)
<strong>Total Dinner Tickets: </strong><% extra_dinners + rego_nonspeaker['Professional'] + speakers_registered %><br>
-->
<br>
<!-- <strong>Total Speakers (hard coded, seven number):</strong> 83<br> -->
<strong>Speakers Registered: </strong><% speakers_registered %><br>
<br>
<strong>Earlybird status:</strong> <% earlybird |h%>,
<% `c.eb` |h%>, <% c.ebtext |h%><br>
<br>
<strong>Money in Bank:</strong> <% h.number_to_currency(money_in_bank) %> <br>
<br>
<& ../accommodation/list.myt, accommodation_paid = accommodation_paid &>

% else:
  <p><strong>No registrations yet</strong></p>
  <p>And now also no divide by zero error or flood of email.</p>
% # endif

<%init>

rego_all = {
    'Hobbyist': 0,
    'Fairy Penguin Sponsor': 0,
    'Professional': 0,
    'Concession': 0,
    'Speaker': 0,
    'Mini-conf organiser': 0,
}
rego_nonspeaker = rego_all.copy()
rego_paid = rego_all.copy()
rego_total = 0
rego_total_nonspeaker = 0
rego_total_paid = 0
speakers_registered = 0
extra_dinners = 0
money_in_bank = 0
accommodation_paid = {}
earlybird = 0

# Loop through regos
for r in c.registration_collection:
    type = r.type

    # All proposals
    rego_all[type] = 1 + rego_all.get(type, 0)
    rego_total += 1;
    extra_dinners += r.dinner

    # Don't count speakers
    speaker = 0;
    if r.person.proposals:
        for proposal in r.person.proposals:
            if proposal.accepted:
                speaker = 1;
    if speaker:
        speakers_registered += 1
    else:
        rego_nonspeaker[type] = 1 + rego_nonspeaker.get(type, 0)
        rego_total_nonspeaker += 1;

    if r.person.invoices and r.person.invoices[0].paid():
        rego_paid[type] += 1
        rego_total_paid += 1
        money_in_bank += r.person.invoices[0].total()/100.0
	if r.accommodation_option_id > 0:
		if r.accommodation_option_id in accommodation_paid:
			accommodation_paid[r.accommodation_option_id] += 1
		else:
			accommodation_paid[r.accommodation_option_id] = 1
	if type in ('Hobbyist', 'Professional') and not speaker:
	    earlybird += 1

from datetime import datetime
if datetime.now() > c.ebdate:
    earlybird = 'too late'
else:
    earlybird = '%d taken' % earlybird

</%init>
