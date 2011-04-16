# File for configuration specific to zookeepr

base_theme = 'default'
theme = 'lca2011'

# File system paths that start with $xxx/ have file_paths['xxx'] prepended
# to them.
file_paths = {
  'zk_root' :           None,
  'public_path':        '$zk_root/zookeepr/public',
  'public_html':        '',
  'news_fileprefix':    '$public_path/featured',
  'news_htmlprefix':    '/featured',
  # Points towards where the slides and other recordings are stored
  'slides_path':        '$public_path/slides',
  'slides_html':        '/slides',
  # Where photo competition entries are stored.
  'photocomp_path':     '$public_path/photocomp',
  'ogg_path':           'http://mirror.linux.org.au/lca10/videos/ogg',
  'speex_path':         'http://mirror.linux.org.au/lca10/videos/speex',
}
if file_paths.get('zk_root', None) is None:
    file_paths['zk_root'] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for k in file_paths:
    while file_paths[k].startswith("$"):
        file_paths[k] = file_paths[file_paths[k][1:].split('/')[0]] + "/" + file_paths[k].split("/",1)[1]

