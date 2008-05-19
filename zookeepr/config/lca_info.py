# File for holding configuration relative to the current LCA
# This could be dberised sometimes

lca_info = {
# CommSecure (the payment gateway provider) requires a Merchant ID
# and a shared secret
  'commsecure_merchantid' : 'TestZookeeprMerchantID',
  'commsecure_secret' : 'zing',

# Contact email for the committee
  'contact_email' : 'josh@nitrotech.org',
  'event_name' : 'linux.conf.au 2009',

# Possible statuses not_open|open|closed
  'cfp_status' : 'not_open',
  'cfmini_status' : 'open',
  'registration_status' : 'not_open',
# Wether we are collecting miniconfs or papers.
  'mini_conf_email' : 'miniconfs@marchsouth.org',
  
# Available Tickets
  'total_ticets' = 700,
  'speakers_coming' = 70 # hard coded to the number of speakers... do we need this since speakers register?
}

