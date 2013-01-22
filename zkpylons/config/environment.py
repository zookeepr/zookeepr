"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons import config
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

import zkpylons.lib.app_globals as app_globals
import zkpylons.lib.helpers
from zkpylons.config.routing import make_map
from zkpylons.model import init_model

from zkpylons.config.lca_info import lca_info
from zkpylons.config.zkpylons_config import file_paths

from pylons.configuration import PylonsConfig

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
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

    # Setup the SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    
    return config

config = PylonsConfig()
