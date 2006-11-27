<h1> Registration Report </h1>


<h2> Total Registrations </h2>
<table> 
    <tr>
        <th>Type</th>
        <th>Num (Inc Speakers)</th>
        <th>Numr (Ex Speakers)</th>
        <th>Num Paid</th>
        <th>Percentage Paid</th>
        <th>Attendees Breakdown</th>
    </tr>

% for type in rego_all:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><% type %></td>
        <td><% rego_all[type] %></td>
        <td><% rego_nonspeaker[type] %></td>
        <td><% rego_paid[type] %></td>
        <td><% h.number_to_percentage(rego_paid[type]*100/rego_total_nonspeaker, precision=0) %></td>
        <td><% h.number_to_percentage(rego_nonspeaker[type]*100/rego_total_nonspeaker, precision=0) %></td>
    </tr>
% #endfor

<tr>
    <td><strong>Total</strong></td>
    <td><strong><% rego_total %></strong></td>
    <td><strong><% rego_total_nonspeaker %></strong></td>
    <td><strong><% rego_total_paid %></strong></td>
    <td><strong><% h.number_to_percentage(rego_total_paid*100/rego_total_nonspeaker, precision=0) %></strong></td>
    <td><strong><% h.number_to_percentage(100, precision=0) %></strong></td>
</tr>

</table>

<strong>Extra Dinner Tickets: </strong><% extra_dinners %><br>
<strong>Total Dinner Tickets: </strong><% extra_dinners + rego_nonspeaker['Professional'] + speakers_registered %><br>
<br>
<strong>Total Speakers (hard coded):</strong> 83<br>
<strong>Speakers Registered: </strong><% speakers_registered %><br>
<br>
<strong>Money in Bank:</strong> <% h.number_to_currency(money_in_bank) %> <br>
<br>
<& ../accommodation/list.myt &>

<%init>

rego_all = {
    'Hobbyist': 0,
    'Professional': 0,
    'Concession': 0,
}
rego_nonspeaker = rego_all.copy()
rego_paid = rego_all.copy()
rego_total = 0
rego_total_nonspeaker = 0
rego_total_paid = 0
speakers_registered = 0
extra_dinners = 0
money_in_bank = 0

# Loop through regos
for r in c.registration_collection:
    type = r.type

    # All proposals
    rego_all[type] += 1
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
        rego_nonspeaker[type] += 1
        rego_total_nonspeaker += 1;

    if r.person.invoices and r.person.invoices[0].good_payments:
        rego_paid[type] += 1
        rego_total_paid += 1
        money_in_bank += r.person.invoices[0].total()/100.0;




</%init>
