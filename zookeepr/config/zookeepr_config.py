# File for configuration specific to zookeepr

import os

# File system paths that start with $xxx/ have file_paths['xxx'] prepended
# to them.
file_paths = {
  'zk_root' :           None,
  'base_templates' :    '$zk_root/zookeepr/templates',
  'base_public':        '$zk_root/zookeepr/public',
  'theme_root' :        '$zk_root/zookeepr/themes',
  'base_theme' :        '$zk_root/zookeepr/templates',
  'enabled_theme':      '$theme_root/lca2012',
  'theme_templates':    '$enabled_theme/templates',
  'theme_public':       '$enabled_theme/public',
  'public_html':        '',
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

