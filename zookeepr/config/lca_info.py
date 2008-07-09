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
  'registration_status' : 'not_open',
# Wether we are collecting miniconfs or papers.
  'mini_conf_email' : 'miniconfs@marchsouth.org',

}

lca_rego = { 
# Id's used for speaker accom
	'speaker_accom_options' : (51,52,53),

# Date Early Bird ends
	'earlybird_enddate' : datetime(2008, 11, 18, 00, 00, 00),
	'earlybird_limit' : 220
}

file_paths = {
    'public_path': '/home/josh/LCA09/website/db_content/zookeepr/public',
    'public_html': '',
    'news_fileprefix': '/home/josh/LCA09/website/db_content/zookeepr/public/featured',
    'news_htmlprefix': '/featured'
}

lca_menu = [
    ('Home', '/home', 'home'),
    ('About', '/about/the_event_history', 'about'),
    ('Sponsors', '/sponsors/become_a_sponsor', 'sponsors'),
    ('Programme/Participate', '/programme/about_programme', 'programme'),
    #('Register', '/register', 'register'), # -- Stage 2
    #('Wiki', '/wiki', 'wiki'),
    ('Media', '/media/news', 'media'),
    ('Contact', '/contact', 'contact'),
]

lca_submenus = {
  'about': ['The event/history', 'Tasmania/Hobart', 'Venue', 'Linux/Open Source'],
  'sponsors': ['Become a Sponsor'],
  'programme': ['About Programme', 'Submit a miniconf', 'Submit a Presentation', 'Edit Submission', 'Presenter FAQ'], # stage 1
  #'programme': ['About Programme', 'miniconfs','Schedule','Official social events','Open day'], # stage 2
  #'register': ['Prices/Ticket types','Terms and Conditions','Accommodation','Partners programme'], # stage 2
  'media': ['News','In the press']
}
