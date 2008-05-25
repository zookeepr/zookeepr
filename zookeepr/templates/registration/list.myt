<h1> Registration Report </h1>


<h2> Total Registrations </h2>

% if rego_total > 0:

<table> 
    <tr>
        <th>Type</th>
        <th colspan="2">Normal</th>
        <th>Speakers</th>
        <th>Total</th>
        <th>Keynote</th>
    </tr>
%   total_chart = []
%   keynote_chart = []
%   for type in rego_types:
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
%     total_chart.append((type, float(rego_all[type])))
%     if type in keynote_types:
        <td><% keynote[type] %></td>
%       keynote_chart.append((type, float(str(keynote[type]).split(' ')[0])))
%     else:
        <td>-</td>
%     #endif
    </tr>
%   #endfor

<tr>
    <td><strong>Total</strong></td>
    <td><strong><% rego_total_nonspeaker %></strong></td>
    <td><strong><% h.number_to_percentage(100, precision=0) %></strong></td>
    <td><strong><% speakers_registered %></strong></td>
    <td><strong><% rego_total %></strong></td>
    <td><strong><% keynote_total %></strong></td>
</tr>

</table>
<table>
<tr><th>Total</th><th>Keynote</th></tr>
<tr>
  <td> <img width="400" height="200" src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:<% ','.join([str(count/rego_total) for (label, count) in total_chart]) %>&chl=<% '|'.join([label for (label, count) in total_chart]) %>"></td>
  <td> <img width="400" height="200" src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:<% ','.join([str(count/keynote_total) for (label, count) in keynote_chart]) %>&chl=<% '|'.join([label for (label, count) in keynote_chart]) %>"></td>
</table>

<br>
<strong>Extra Dinner Tickets: </strong><% extra_dinners %><br>

<!-- (seven calculation, ours is different)
<strong>Total Dinner Tickets: </strong><% extra_dinners + rego_nonspeaker['Professional'] + speakers_registered %><br>
-->

<br>
<strong>Earlybird status:</strong> <% earlybird |h%>,
available=<% `c.eb` |h%>, <% c.ebtext |h%><br>
("Taken" figure includes 20 for google but not catalyst or SGI.)
<br>
<br>
<strong>Ceiling status:</strong> <% `c.ceiling.__dict__` |h%>
<br>
<br>
%   test_payments = 11.20
%   non_d1_payments = 1196.80 + 671.60
<strong>Money in Bank:</strong>
<% h.number_to_currency(money_in_bank + test_payments) %>
(including <% h.number_to_currency(test_payments) %> of test payments; this is 
<% h.number_to_currency(non_d1_payments) %> +
<% h.number_to_currency(money_in_bank + test_payments - non_d1_payments) %>,
the latter of which should agree with DirectOne's "Paid/Real Invoices" total)
<br>
<br>
<strong>Google voucher code:</strong> <% google |h %> used
<br>
<br>
<& ../accommodation/list.myt, accommodation_paid = accommodation_paid &>

% else:
  <p><strong>No registrations yet</strong></p>
  <p>And now also no divide by zero error or flood of email.</p>
% # endif

<%init>

keynote_types = (
    'Fairy Penguin Sponsor',
    'Professional',
    'Hobbyist',
    'Concession',
    'Student',
    'Speaker',
    'Mini-conf organiser',
    'Unused voucher codes',
)
rego_types = (
    'Fairy Penguin Sponsor',
    'Professional',
    'Hobbyist',
    'Concession',
    'Student',
    'Speaker',
    'Mini-conf organiser',
    'Team',
    'Monday pass',
    'Tuesday pass',
    'Monday only',
    'Tuesday only',
    'Professional - No Keynote Access',
    'Hobbyist - No Keynote Access',
    'Student - No Keynote Access',
    'Volunteer',
    'Penguin Dinner only',
    'Unused voucher codes',
)
rego_all = {}
for t in rego_types:
    rego_all[t] = 0
keynote = {}
for t in keynote_types:
    keynote[t] = 0

rego_nonspeaker = rego_all.copy()
rego_speaker = rego_all.copy()
rego_paid = rego_all.copy()
rego_total = 0
rego_total_nonspeaker = 0
rego_total_paid = 0
keynote_total = 0
speakers_registered = 0
extra_dinners = 0
money_in_bank = 0
accommodation_paid = {}
earlybird = 0
google = 0
speaker_keynote_reduce = 0

# Loop through regos
for r in c.registration_collection:
    if r.type=='Cancelled':
        continue
    speaker = r.person.is_speaker()
    paid = r.person.invoices and r.person.invoices[0].paid()

    if r.voucher_code and r.voucher_code.startswith('GOOGLE-'):
        google += 1

    # skip unpaid registrations, except speakers
    if not (paid or speaker):
      continue

    type = r.type

    if speaker and not paid:
      # until they pay, their ticket type is effectively "Speaker"
      type = 'Speaker'

    # All proposals
    rego_all[type] = 1 + rego_all.get(type, 0)
    rego_total += 1
    if r.dinner != None:
    	extra_dinners += r.dinner

    # Don't count speakers
    if speaker:
        speakers_registered += 1
        rego_speaker[type] = 1 + rego_speaker.get(type, 0)
	if type!='Speaker' and type in keynote_types:
	    speaker_keynote_reduce += 1
    else:
        rego_nonspeaker[type] = 1 + rego_nonspeaker.get(type, 0)
        rego_total_nonspeaker += 1;

    if r.type in keynote_types:
        keynote[r.type] += 1
	keynote_total += 1

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
        if r.voucher_code and r.voucher_code.startswith('GOOGLE-'):
	    pass
        else:
	    earlybird += 1


unused = c.ceiling.vouchers - c.ceiling.disc_regos
rego_nonspeaker['Unused voucher codes'] += unused
rego_all['Unused voucher codes'] += unused
keynote['Unused voucher codes'] += unused
rego_total_nonspeaker += unused
rego_total += unused
keynote_total += unused

fixed_speakers = 74 - speaker_keynote_reduce
keynote_total += fixed_speakers - keynote['Speaker']
keynote['Speaker'] = '%d (hardcoded)' % fixed_speakers

fixed_mcorgs = 20
keynote_total += fixed_mcorgs - keynote['Mini-conf organiser']
keynote['Mini-conf organiser'] = '%d (hardcoded)' % fixed_mcorgs

earlybird += 20 # the GOOGLE group booking is deemed all taken

from datetime import datetime
if datetime.now() > c.ebdate:
    earlybird = 'too late'
else:
    earlybird = '%d taken' % earlybird

</%init>
