# File for holding configuration relative to the current LCA
# This could be dberised sometimes
from datetime import datetime


lca_info = {
# CommSecure (the payment gateway provider) requires a Merchant ID
# and a shared secret
  'commsecure_merchantid' : 'TestZookeeprMerchantID',
  'commsecure_secret' : 'zing',

# Contact email for the committee
  'contact_email' : 'josh@nitrotech.org',

# Event information
  'event_name' : 'linux.conf.au 2009',
  'date' : datetime(2009, 1, 19, 9, 0, 00),

# Possible statuses not_open|open|closed
  'cfp_status' : 'closed',
  'cfmini_status' : 'open',
  'registration_status' : 'not_open',
# Wether we are collecting miniconfs or papers.
  'mini_conf_email' : 'miniconfs@marchsouth.org',

}

