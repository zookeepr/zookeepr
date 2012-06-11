# File for configuration specific to zkpylons

import os

# File system paths that start with $xxx/ have file_paths['xxx'] prepended
# to them.
file_paths = {
  'zk_root' :           None,  				# None will use the folder 2 above this one
  'base_templates' :    '$zk_root/zkpylons/templates',
  'base_public':        '$zk_root/zkpylons/public',
  'theme_root' :        '$zk_root/zkpylons/themes',
  'enabled_theme':      '$theme_root/zkpylons',
  'theme_templates':    '$enabled_theme/templates',
  'theme_public':       '$enabled_theme/public',
  'public_html':        '',
  'public_path':        '$enabled_theme/public',                # this is for uploadable content... 
  'news_fileprefix':    '$base_public/featured',
  'news_htmlprefix':    '/featured',
  # Points towards where the slides and other recordings are stored
  'slides_path':        '$base_public/slides',
  'slides_html':        '/slides',
  # Where photo competition entries are stored.
  'photocomp_path':     '$base_public/photocomp',
  'ogg_path':           'http://mirror.linux.org.au/lca10/videos/ogg',
  'speex_path':         'http://mirror.linux.org.au/lca10/videos/speex',
}


if file_paths.get('zk_root', None) is None:
    file_paths['zk_root'] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for k in file_paths:
    while file_paths[k].startswith("$"):
        file_paths[k] = file_paths[file_paths[k][1:].split('/')[0]] + "/" + file_paths[k].split("/",1)[1]

