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
  'cfp_status' : 'open',
  'cfmini_status' : 'open',
  'registration_status' : 'open',
# Wether we are collecting miniconfs or papers.
  'mini_conf_email' : 'miniconfs@marchsouth.org',

  'lca_rego' : { 
# Id's used for speaker accom
	'speaker_accom_options' : (51,52,53),

# Date Early Bird ends
	'earlybird_enddate' : datetime(2008, 11, 18, 00, 00, 00),
	'earlybird_limit' : 220
  }
}
