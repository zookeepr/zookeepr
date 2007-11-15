<h1> Registration Report </h1>


<h2> Total Registrations </h2>

% if rego_total > 0:

<table> 
    <tr>
        <th>Type</th>
        <th colspan="2">Normal</th>
        <th>Speakers</th>
        <th>Total</th>
    </tr>
%   for type in rego_all:
    <tr class="<% h.cycle('even', 'odd')%> ">
        <td><% type %></td>
        <td><% rego_nonspeaker.get(type, '-') %></td>
%     if rego_total_nonspeaker > 0:
        <td><% h.number_to_percentage(rego_nonspeaker.get(type,0)*100/rego_total_nonspeaker, precision=0) %></td>
%     else:
        <td>-</td>
%     #endif
        <td><% rego_speaker.get(type, '-') %></td>
        <td><% rego_all[type] %></td>
    </tr>
%   #endfor

<tr>
    <td><strong>Total</strong></td>
    <td><strong><% rego_total_nonspeaker %></strong></td>
    <td><strong><% h.number_to_percentage(100, precision=0) %></strong></td>
    <td><strong><% speakers_registered %></strong></td>
    <td><strong><% rego_total %></strong></td>
</tr>

</table>

<strong>Extra Dinner Tickets: </strong><% extra_dinners %><br>

<!-- (seven calculation, ours is different)
<strong>Total Dinner Tickets: </strong><% extra_dinners + rego_nonspeaker['Professional'] + speakers_registered %><br>
-->

<br>
<strong>Earlybird status:</strong> <% earlybird |h%>,
available=<% `c.eb` |h%>, <% c.ebtext |h%><br>
<br>
%   test_payments = 11.20
<strong>Money in Bank:</strong>
<% h.number_to_currency(money_in_bank + test_payments) %>
(including <% h.number_to_currency(test_payments) %> of test payments, so
this number should agree with DirectOne's "Paid/Real Invoices" total)
<br>
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
    'Student': 0,
    'Speaker': 0,
    'Mini-conf organiser': 0,
    'Team': 0,
}
rego_nonspeaker = rego_all.copy()
rego_speaker = rego_all.copy()
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
    speaker = r.person.is_speaker()
    paid = r.person.invoices and r.person.invoices[0].paid()

    # skip unpaid registrations, except speakers
    if not (paid or speaker):
      continue

    type = r.type

    if speaker and not paid:
      # until they pay, their ticket type is effectively "Speaker"
      type = 'Speaker'

    # All proposals
    rego_all[type] = 1 + rego_all.get(type, 0)
    rego_total += 1;
    extra_dinners += r.dinner

    # Don't count speakers
    if speaker:
        speakers_registered += 1
        rego_speaker[type] = 1 + rego_speaker.get(type, 0)
    else:
        rego_nonspeaker[type] = 1 + rego_nonspeaker.get(type, 0)
        rego_total_nonspeaker += 1;

    for i in r.person.invoices:
      if i.paid():
        money_in_bank += i.total()/100.0
    rego_paid[type] += 1
    rego_total_paid += 1
    if r.accommodation_option_id > 0:
	    if r.accommodation_option_id in accommodation_paid:
		    accommodation_paid[r.accommodation_option_id] += 1
	    else:
		    accommodation_paid[r.accommodation_option_id] = 1
    if type in ('Hobbyist', 'Professional') and not speaker:
        if r.discount_code and r.discount_code.startswith('GOOGLE-'):
	    pass
        else:
	    earlybird += 1

earlybird += 20 # the GOOGLE group booking is deemed all taken

from datetime import datetime
if datetime.now() > c.ebdate:
    earlybird = 'too late'
else:
    earlybird = '%d taken' % earlybird

</%init>
