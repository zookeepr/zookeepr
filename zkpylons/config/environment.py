"""Pylons environment configuration"""
import os
import re
import sys

from mako.lookup import TemplateLookup
from mako import exceptions
from pylons import config
import sqlalchemy

import zkpylons.lib.app_globals as app_globals
import zkpylons.lib.helpers
from zkpylons.config.routing import make_map
from zkpylons.model import init_model
from zkpylons.model.config import Config

from zkpylons.config.zkpylons_config import initialise_file_paths

from pylons.configuration import PylonsConfig


def handle_mako_error(context, exc):
    # Three term exception should put the Mako stack in as the exception stack trace
    # Unfortunately it doesn't work, or it gets rewritten again
    print (exceptions.text_error_template().render())

    st = sys.exc_traceback
    raise (exc, None, st)


def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """

    # Setup the SQLAlchemy database engine manually (rather than 'from config')
    # so that we can pull the theme out before we set up the pylons app
    engine = sqlalchemy.create_engine(app_conf['sqlalchemy.url'])
    init_model(engine)

    file_paths = initialise_file_paths()

    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=[file_paths['theme_public'], file_paths['base_public']],
                 templates=[file_paths['base_templates']],           # apparently pylons still wants this and as a list
                 base_templates=file_paths['base_templates'],
                 theme_templates=file_paths['theme_templates'])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='zkpylons', paths=paths)

    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    
    config['pylons.h'] = zkpylons.lib.helpers
    config['pylons.strict_tmpl_context'] = False

    config['pylons.package'] = 'zkpylons'

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=[paths['theme_templates'], paths['base_templates']],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    
    return config

config = PylonsConfig()
