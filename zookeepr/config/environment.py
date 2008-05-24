import sys
import os

import pylons.config
import webhelpers

from pylons import config

import zookeepr.lib.app_globals as app_globals
import zookeepr.lib.helpers

from zookeepr.config.routing import make_map
from zookeepr.config.lca_info import lca_info

def load_environment(global_conf, app_conf):
    # Setup our paths
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = {'root': root_path,
             'controllers': os.path.join(root_path, 'controllers'),
             'templates': [os.path.join(root_path, path) for path in \
                           ('components', 'templates')],
             'static_files': os.path.join(root_path, 'public')
             }

    sys.path.insert(0, os.path.join(root_path, 'config'))

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='zookeepr',
                    template_engine='pylonsmyghty', paths=paths)

    config['pylons.g'] = app_globals.Globals(global_conf, app_conf)
    config['pylons.h'] = zookeepr.lib.helpers
    config['routes.map'] = make_map()
    tmpl_options = pylons.config['buffet.template_options']
    
    # The following options are passed directly into Myghty, so all configuration options
    # available to the Myghty handler are available for your use here
    myghty = {}
    myghty['log_errors'] = True

    # Add webhelpers' auto_link and simple_format methods to myghty's
    # escaping functions, for great justice.
    # http://www.myghty.org/docs/filtering.myt#filtering_escaping_custom
    myghty['escapes'] = {'l': webhelpers.auto_link,
                         's': webhelpers.simple_format
                         }
    
    # Add your own Myghty config options here, note that all config options will override
    # any Pylons config options
    
    # Return our loaded config object
    # (no longer needed in new pylons --Jiri 27.4.2008)
    #return pylons.config.Config(myghty, map, paths)
