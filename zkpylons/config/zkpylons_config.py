# File for configuration specific to zkpylons

import os
import re

from zkpylons.model.config import Config


# File system paths that start with $xxx/ have file_paths['xxx'] prepended
# to them.
# Can't use DB config table as the models are not loaded yet
file_paths = {
  # None will use the folder 2 above this one
  'zk_root' :           None,
  'base_templates' :    '$zk_root/zkpylons/templates',
  'base_public':        '$zk_root/zkpylons/public',
  'theme_root' :        '$zk_root/zkpylons/themes',
  'theme_templates':    '$enabled_theme/templates',
  'theme_public':       '$enabled_theme/public',
  'public_html':        '',
   # this is for uploadable content
  'public_path':        '$enabled_theme/public',
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
    file_paths['zk_root'] = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))


def expand_variable(value):
    for substitute in re.findall('\$([A-Za-z_]*)', value):
        if substitute in file_paths:
            value = re.sub('\$' + substitute, file_paths[substitute], value)
            value = expand_variable(value)
    return value


for k in file_paths:
    file_paths[k] = expand_variable(file_paths[k])


def initialise_file_paths():
    # Should be called after db is initialised
    if 'enabled_theme' not in file_paths:
        enabled_theme = Config.get('theme')
        file_paths['enabled_theme'] = os.path.join(file_paths['theme_root'], enabled_theme)
        for k in file_paths:
            file_paths[k] = re.sub('\$enabled_theme', file_paths['enabled_theme'], file_paths[k])
    return file_paths


def get_path(key):
    return initialise_file_paths()[key]
