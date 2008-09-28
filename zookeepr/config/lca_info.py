# File for holding configuration relative to the current LCA
# This could be dberised sometimes
from datetime import datetime


lca_info = {
# CommSecure (the payment gateway provider) requires a Merchant ID
# and a shared secret
  'commsecure_merchantid' : 'TestZookeeprMerchantID',
  'commsecure_secret' : 'zing',

# Contact email for the committee
  'contact_email' : 'joshua.hesketh@marchsouth.org',

# Event information
  'event_parent_organisation' : 'Linux Australia, Incorporated',
  'event_parent_url' : 'http://www.linux.org.au/',
  'event_name' : 'linux.conf.au 2009',
  'event_url' : 'http://www.linux.conf.au/',
  'event_tax_number' : 'ABN 56 987 117 479',
# 'event_tax_number' : 'NZ GST #90-792-369',
  'event_postal_address' : '25 Wellington St North Hobart TAS 7000, Australia',
  'event_fax_number' : '+61 3 6234 1262',
  'event_phone_number': '+61 432 996 932',
  'date' : datetime(2009, 1, 19, 9, 0, 00),

  'invoice_message' : 'To qualify for the earlybird discount you must have registered and paid by the 27th of October (unless earlybird tickets sell out earlier).',

# Possible statuses not_open|open|closed
  'cfp_status' : 'closed',
  'cfmini_status' : 'closed',
  'paper_editing' : 'closed',
# Wether we are collecting miniconfs or papers.
  'mini_conf_email' : 'miniconfs@marchsouth.org',

}

lca_rego = {
  'miniconfs' : (
              ('Monday',('Open Source Database', 'Kernel', 'Sysadmin', 'Virtualisation', 'MythTV', 'Gaming', 'Free as in Freedom', 'Mobile devices')),
              ('Tuesday',('Open Source Database', 'Linux Security', 'Sysadmin', 'Multimedia', 'Linuxchix', 'Gaming', 'Business of Software development', 'Mobile devices'))
             ),
  'shells' : ['bash', 'busybox', 'csh', 'dash', 'emacs', 'ksh', 'sh', 'smrsh', 'tcsh', 'XTree Gold', 'zsh'],
  'editors' : ['bluefish', 'emacs', 'gedit', 'jed', 'kate', 'nano', 'vi', 'vim', 'xemacs'],
  'distros' : ['CentOS', 'Darwin', 'Debian', 'Fedora', 'FreeBSD', 'Gentoo', 'L4', 'Mandriva', 'NetBSD', 'Nexenta', 'OpenBSD', 'OpenSolaris', 'OpenSUSE', 'Oracle Enterprise Linux', 'RHEL', 'Slackware', 'Ubuntu'],
  'past_confs' : [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)'), ('07', '2007 (Sydney)'), ('08', '2008 (Melbourne)')],

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
  'public_path': '/home/josh/LCA09/website/db_content/zookeepr/public',
  'public_html': '',
  'news_fileprefix': '/home/josh/LCA09/website/db_content/zookeepr/public/featured',
  'news_htmlprefix': '/featured'
}

lca_menu = [
  ('Home', '/home', 'home'),
  ('About', '/about/the_event_history', 'about'),
  ('Sponsors', '/sponsors/become_a_sponsor', 'sponsors'),
  ('Programme', '/programme/about_programme', 'programme'),
  ('Register', '/register/prices_ticket_types', 'register'), # -- Stage 2
  ('Wiki', '/wiki', 'wiki'),
  ('Media', '/media/news', 'media'),
  ('Contact', '/contact', 'contact'),
]

lca_submenus = {
  'about': ['The event/history', 'Tasmania/Hobart', 'Venue', 'Linux/Open Source'],
  'sponsors': ['Become a Sponsor'],
  #'programme': ['About Programme', 'Submit a miniconf', 'Submit a Presentation', 'Edit Submission', 'Presenter FAQ'], # stage 1
  'programme': ['About Programme', 'miniconfs','Schedule','Official social events','Open day'], # stage 2
  'register': ['Prices/Ticket types','Terms and Conditions','Accommodation','Partners programme'], # stage 2
  'media': ['News','In the press']
}
