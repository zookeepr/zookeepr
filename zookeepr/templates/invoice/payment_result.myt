<h3>Payment result

% for k in request.GET:
   <% k %>: <% request.GET[k] %><br>
% # end_for

Result: <% result %>


<%init>
import hmac, sha

# Test.
merchantid = 'Testlinuxlca'
secret = 'ASK_JF'

# Live.
#merchantid = 'linuxlca'
#secret = 'ASK_JF'


keys = request.GET.keys()
keys.sort()
stringToMAC = '&'.join(['%s=%s' % (key, request.GET[key]) for key in keys if key != 'MAC'])
mac = hmac.new(secret, stringToMAC, sha).hexdigest()
result = 'BAD'
if mac.lower() == request.GET['MAC'].lower():
   result = 'GOOD'

</%init>


