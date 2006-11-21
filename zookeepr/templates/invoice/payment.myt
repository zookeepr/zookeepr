<form method="POST" action="https://clearance.commsecure.com.au/cgi-bin/PSCheckout">

% for k in fields.keys():
    <input type="hidden" name="<% k %>" value="<% fields[k] %>">
% # end for

<input type="submit" value="Pay via PaySecure Checkout">
</form>

<%init>
import hmac, sha

# Test 
merchantid = 'Testlinuxlca'
secret = 'ASK_JF'

# Live 
#merchantid = 'linuxlca'
#secret = 'ASK_JF'

# Generate a unique payment ID
paymentid = 1

# amount in cents
amount = 69000

# Generate a uniq invoice ID
invoiceid = 1000

fields = {
    'MerchantID': merchantid,
    'PaymentID': paymentid
    'Amount': amount
    'InvoiceID': invoiceid
}

# Generate HMAC
keys = fields.keys()
keys.sort()     # keys in alphabetical order

# key1=value1&key2=value2&key3=value3 ...
stringToMAC = '&'.join(['%s=%s' % (key, fields[key]) for key in keys])
mac = hmac.new(secret, stringToMAC, sha).hexdigest()
fields['MAC'] = mac

</%init>


