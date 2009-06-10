# File for holding configuration relative to the current LCA
# This could be dberised sometimes
from datetime import datetime


lca_info = {
# CommSecure (the payment gateway provider) requires a Merchant ID
# and a shared secret
  'commsecure_merchantid' : 'TestZookeeprMerchantID',
  'commsecure_secret' : 'zing',

# Contact email for the committee
  'contact_email' : 'contact@lca2010.org.nz',
# All email sent by ZK will Bcc here:
  'bcc_email' : 'bcc_archive@lca2010.org.nz',
  'webmaster_email': 'webmaster@lca2010.org.nz',

# Event information
  'event_parent_organisation' : 'Linux Australia, Incorporated',
  'event_parent_url' : 'http://www.linux.org.au/',
  'event_name' : 'linux.conf.au 2010',
  'event_shortname' : 'lca2010',
  'event_url' : 'http://www.lca2010.org.nz/',
#  'event_tax_number' : 'ABN 56 987 117 479',
 'event_tax_number' : 'NZ GST #90-792-369',
  'event_postal_address' : 'PO Box 11-682, Manners St, Wellington, NEW ZEALAND 6142',
  'event_fax_number' : '+64 4 802 0422',
  'event_phone_number': '+64 4 802 0422',
  'date' : datetime(2010, 1, 17, 9, 0, 00),
  'media_license' : 'Creative Commons ShareAlike License',

  'invoice_message' : 'To qualify for the earlybird discount you must have registered and paid by the 27th of October (unless earlybird tickets sell out earlier).',

# Possible statuses not_open|open|closed
  'cfp_status' : 'not_open',
  'cfmini_status' : 'not_open',
  'paper_editing' : 'not_open',
  'conference_status': 'not_open',

  'mini_conf_email' : 'miniconfs@lca2010.org.nz',
  'speaker_email' : 'speakers@lca2010.org.nz',

  'emails': {
     'presentation' : 'speakers@lca2010.org.nz',
     'tutorial'     : 'speakers@lca2010.org.nz',
     'miniconf'     : 'miniconfs@lca2010.org.nz',
  },

  'proposal_update_email': 'puck@lca2010.org.nz', # recieve notifications when proposals are changed. Leave blank for none.
}

lca_rego = {
  'volunteer_areas': (
            {'name': 'Administration', 'description': 'Take care and help out on any administration tasks.'},
            {'name': 'Registration Desk', 'description': 'Sign people into the conference and help with general enquires.'},
            {'name': 'Audio+Video', 'description': 'Help out with filming and/or encoding various talks and presentations.'},
            {'name': 'Network Helper', 'description': 'Assist in setting up and running the network.'},
            {'name': 'Partners Programme Helper', 'description': 'Help out with the daily activities on the partners programme.'},
            {'name': 'Runner', 'description': 'Move items around, help conference organisers, find things and do general jobs given to you.'},
            {'name': 'Venue Helper', 'description': 'Help with setting up break times, tables and chairs and other miscellaneous things.'},
            {'name': 'Usher', 'description': 'Introduce speakers and manage rooms, keeping them to a schedule.'},
            {'name': 'Driver', 'description': 'Have driver\'s licence, will travel to help pick up items and shuttle VIP\'s.'},
            {'name': 'Car', 'description': 'Have car and can be a driver.'},
            {'name': 'Week Before', 'description': 'Available during the week before the conference (x-y Jan).'},
            {'name': 'Week After', 'description': 'Available during the week after the conference (a-c Jan).'},
            {'name': 'Packout', 'description': 'Available to help pack-out of the venue on Saturday and Sunday.'},
        ),
  'miniconfs' : (
              ('Monday',('Open Source Database', 'Kernel', 'Sysadmin', 'MythTV', 'Linuxchix', 'Mobile devices', 'Business of Software development')),
              ('Tuesday',('Open Source Database', 'Linux Security', 'Sysadmin', 'Multimedia', 'Virtualisation', 'Gaming', 'Free as in Freedom'))
             ),
  'shells' : ['bash', 'busybox', 'csh', 'dash', 'emacs', 'ksh', 'sh', 'smrsh', 'tcsh', 'XTree Gold', 'zsh'],
  'editors' : ['bluefish', 'eclipse', 'emacs', 'gedit', 'jed', 'kate', 'nano', 'vi', 'vim', 'xemacs'],
  'distros' : ['CentOS', 'Darwin', 'Debian', 'Fedora', 'FreeBSD', 'FreeDOS', 'Gentoo', 'L4', 'Mandriva', 'Minix', 'NetBSD', 'Nexenta', 'OpenBSD', 'OpenSolaris', 'OpenSUSE', 'Oracle Enterprise Linux', 'RHEL', 'Slackware', 'Ubuntu'],
  'past_confs' : [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)'), ('07', '2007 (Sydney)'), ('08', '2008 (Melbourne)'), ('09', '2009 (Hobart)')],

  'silly_description' : {
        'starts' : ["a", "a", "a", "one", "no"], # bias toward "a"
        'adverbs' : ["strongly",
               "poorly", "badly", "well", "dynamically",
               "hastily", "statically", "mysteriously",
               "buggily", "extremely", "nicely", "strangely",
               "irritatingly", "unquestionably", "clearly",
               "plainly", "silently", "abstractly", "validly",
               "invalidly", "immutably", "oddly", "disturbingly",
               "atonally", "randomly", "amusingly", "widely",
               "narrowly", "manually", "automatically", "audibly",
               "brilliantly", "independently", "definitively",
               "provably", "improbably", "distortingly",
               "confusingly", "decidedly", "historically",
               "shiny", "troublesome"],
        'adjectives' : ["invalid", "valid",
               "referenced", "dereferenced", "unreferenced",
               "illegal", "legal",
               "questionable",
               "alternate", "implemented", "unimplemented",
               "terminal", "non-terminal",
               "static", "dynamic",
               "qualified", "unqualified",
               "constant", "variable",
               "volatile", "non-volatile",
               "abstract", "concrete",
               "fungible", "non-fungible",
               "untyped", "variable",
               "mutable", "immutable",
               "sizable", "minuscule",
               "perverse", "immovable",
               "compressed", "uncompressed",
               "surreal", "allegorical",
               "trivial", "nontrivial"],
        'nouns' : ["pointer", "structure",
               "definition", "declaration", "type", "union",
               "coder", "admin", "hacker", "kitten", "mistake",
               "conversion", "implementation", "design", "analysis",
               "neophyte", "expert", "bundle", "package",
               "abstraction", "theorem", "display", "distro",
               "restriction", "device", "function", "reference",
               "alien"]
    }
}

file_paths = {
  'zk_root' : '/home/zookeepr/zookeepr/lca10',
  'public_path': '/home/zookeepr/zookeepr/lca10/zookeepr/public',
  'public_html': '',
  'news_fileprefix': '/home/zookeepr/zookeepr/lca10/zookeepr/public/featured',
  'news_htmlprefix': '/featured',
  # Points towards where the slides and other recordings are stored
  'slides_path': '/home/zookeepr/zookeepr/lca10/zookeepr/public/slides',
  'slides_html': '/slides',
  'ogg_path': 'http://mirror.linux.org.au/lca10/videos/ogg',
  'ogg_file_list': '/home/zookeepr/zookeepr/lca10/zookeepr/config/data.txt',
  'speex_path': 'http://mirror.linux.org.au/lca10/videos/speex',
  'speex_file_list': '/home/zookeepr/zookeepr/lca10/zookeepr/config/data.txt',
}

lca_menu = [
  #('Home', '/home', 'home'),
  ('About', '/about/linux.conf.au', 'about'),
  ('Wellington', '/wellington/about_wellington', 'wellington'),
  ('Sponsors', '/sponsors/why_sponsor', 'sponsors'),
  #('Sponsors', '/sponsors/sponsors', 'sponsors'),
  ('Programme', '/programme/about_programme', 'programme'),
  #('Register', '/register/prices_ticket_types', 'register'), # -- Stage 2
  #('Wiki', '/wiki', 'wiki'),
  ('Media', '/media/news', 'media'),
  ('Contact', '/contact', 'contact'),
  ('Planet', 'http://planet.lca2010.org.nz', 'planet'),
]

lca_submenus = {
  'about': ['linux.conf.au', 'Capital Cabal', 'Venue', 'History', 'New Zealand', 'Linux/Open Source'],
  'wellington': ['About Wellington', 'Sightseeing', 'Pre and Post' ],
  'sponsors': ['Why Sponsor'],
  #'sponsors': ['Sponsors', 'Why Sponsor'],
  'programme': ['About', 'Social Events', 'Open Day', 'Partners Programme'], # stage 0
  #'programme': ['About Programme', 'Submit a miniconf', 'Submit a Presentation', 'Edit Submission', 'Presenter FAQ'], # stage 1
  #'programme': ['About Programme', 'miniconfs','Schedule','Official social events','Open day'], # stage 2
  #'register': ['Prices/Ticket types','Terms and Conditions','Accommodation','Partners programme'], # stage 2
  'media': ['News','In the press']
}

