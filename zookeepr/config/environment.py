import sys
import os

import pylons.config
import webhelpers

from zookeepr.config.routing import make_map

def load_environment():
    map = make_map()
    # Setup our paths
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = {'root_path': root_path,
             'controllers': os.path.join(root_path, 'controllers'),
             'templates': [os.path.join(root_path, path) for path in \
                           ('components', 'templates')],
             'static_files': os.path.join(root_path, 'public')
             }
    
    # MoinMoin environment setup, needs to find wikiconfig.py which is in this dir

    sys.path.insert(0, os.path.join(root_path, 'config'))
    
    # The following options are passed directly into Myghty, so all configuration options
    # available to the Myghty handler are available for your use here
    myghty = {}
    myghty['log_errors'] = True

    # Add webhelpers' auto_link and simple_format methods to myghty's
    # escaping functions, for great justice.
    # http://www.myghty.org/docs/filtering.myt#filtering_escaping_custom
    myghty['escapes'] = {'l': webhelpers.auto_link,
                         's': webhelpers.simple_format,
                         'c': webhelpers.number_to_currency,
                         }
    
    # Add your own Myghty config options here, note that all config options will override
    # any Pylons config options
    
    # Return our loaded config object
    return pylons.config.Config(myghty, map, paths)
