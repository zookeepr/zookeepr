from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.registry import RegistryManager
from paste.deploy.config import ConfigMiddleware, PrefixMiddleware

from paste.pony import PonyMiddleware

from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, StaticJavascripts, error_mapper
import pylons.wsgiapp

import zookeepr.lib.app_globals as app_globals
import zookeepr.lib.helpers

from zookeepr.config.environment import load_environment

def error_mapper_wrapper(code, message, environ, global_conf=None, **kw):
    if code != 404:
        return error_mapper(code, message, environ, global_conf, **kw)

def make_app(global_conf, **app_conf):
    """Create a WSGI application and return it
    
    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.
    """
    
    # Load our Pylons configuration defaults
    from pylons import config 
    load_environment(global_conf, app_conf)
    
    # Load our default Pylons WSGI app and make g available
    app = pylons.wsgiapp.PylonsApp(config,
            #helpers=zookeepr.lib.helpers,
            #g=app_globals.Globals
            )
    app = ConfigMiddleware(app, {'app_conf':app_conf,
        'global_conf':global_conf})
    
    # YOUR MIDDLEWARE
    # Put your own middleware here, so that any problems are caught by the error
    # handling middleware underneath

    # Ponies!
    app = PonyMiddleware(app)
    
    # @@@ Change HTTPExceptions to HTTP responses @@@
    app = httpexceptions.make_middleware(app, global_conf)
    
    # @@@ Error Handling @@@
    app = ErrorHandler(app, global_conf, error_template=error_template,
				       **pylons.config['pylons.errorware'])
    
    # @@@ Static Files in public directory @@@
    static_app = StaticURLParser(pylons.config['pylons.paths']['static_files'])

    # @@@ WebHelper's static javascript files @@@
    javascripts_app = StaticJavascripts()
    
    # @@@ Cascade @@@ 
    app = Cascade([static_app, javascripts_app, app])
    
    app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)

    # PrefixMiddleware fixes up the hostname when zookeepr is being proxied.
    # This is important for constructing absolute filenames (as, for instance,
    # PonyMiddleware does). However, it stuffs up things sometimes,
    # especially on my test box, so make it configurable.
    if not app_conf.has_key('prefixMW_disable'):
      app = PrefixMiddleware(app)
    
    # @@@ Establish the Registry for this application @@@
    app = RegistryManager(app)

    return app
