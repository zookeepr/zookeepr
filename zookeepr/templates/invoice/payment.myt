<h1>Pay invoice</h1>

<form method="POST"
  action="https://vault.safepay.com.au/cgi-bin/test_payment.pl"
  onSubmit="return disableForm(this);" >

% for k in fields.keys():
<input type="hidden" name="<% k %>" value="<% fields[k] %>">
% # end for

<p>
<strong>Invoice #:</strong>
<% fields['InvoiceID'] %>
</p>

<p>
<strong>Amount:</strong>
<% h.number_to_currency(fields['Amount']/100.0) %>
</p>

<p>
<% h.link_to('Go back', url=h.url(action='view')) %> to view invoice details, or <% h.link_to('view registration details', url='/profile') %> before payment.
</p>

<h2>Credit Card Details</h2>

<table >
  <tr valign=baseline>
    <td class="label">Card Number:</td>
    <td class="entries"><INPUT TYPE="TEXT" NAME="card_number" SIZE="20"
    MAXLENGTH="25"> (eg. 4000123456781234)</td>
  </tr>
  <tr valign=baseline>
    <td class="label">CVV Number:</td>
    <td class="entries"><INPUT TYPE="TEXT" NAME="cvv" SIZE="6"
    MAXLENGTH="6"> (<a target="new"
    href="https://vault.safepay.com.au/whatisCVV.html">What is this?</a>)
    </td>
  </tr>
  <tr valign="baseline">
    <td class="label">Card Type:</td>
    <td style="entries">
      <select NAME="card_type">
	<option VALUE="VISA" SELECTED>Visa</option>
	<option VALUE="MASTERCARD" >MasterCard</option>
	<option VALUE="AMEX" >American Express</option>
#         <option VALUE="DCCB" >Diners Club</option>
      </select>
    </td>
  </tr>
  <tr valign="baseline">
    <td class="label"> Expiry:</td>
    <td class="entries">
      <select NAME="card_expiry_month">
	<option VALUE="01">01&nbsp;</option>
	<option VALUE="02">02</option>
	<option VALUE="03">03</option>
	<option VALUE="04">04</option>
	<option VALUE="05">05</option>
	<option VALUE="06">06</option>
	<option VALUE="07">07</option>
	<option VALUE="08">08</option>
	<option VALUE="09">09</option>
	<option VALUE="10">10</option>
	<option VALUE="11">11</option>
	<option VALUE="12">12</option>
      </select>
      /
      <select NAME="card_expiry_year">
	<option VALUE="07">2007&nbsp;</option>
	<option VALUE="08">2008</option>
	<option VALUE="09">2009</option>
	<option VALUE="10">2010</option>
	<option VALUE="11">2011</option>
	<option VALUE="12">2012</option>
	<option VALUE="13">2013</option>
	<option VALUE="14">2014</option>
	<option VALUE="15">2015</option>
	<option VALUE="16">2016</option>
      </select>
    </td>
    </tr>
    <tr valign="baseline">
    <td class="label">Name on Card:</td>
    <td class="entries">
    <INPUT TYPE="text" NAME="card_holder" SIZE="35" MAXLENGTH="50">
    </td>
    </tr>

    <tr valign="baseline">
    <td class="label"><b>Email Address (optional):</b></td>
    <td class="entries">
    <INPUT TYPE="text" NAME="receipt_address" VALUE="" SIZE="35" MAXLENGTH="60">
    </td>
  </tr>
</table>
<br>

<input type="submit" value="Pay via SecurePay"> (please click only once;
processing can take a couple of minutes)
</form>

<%args>
fields
</%args>
