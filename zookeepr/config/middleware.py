from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser

from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, error_mapper
import pylons.wsgiapp
from authkit.middleware import Security, Authenticator, ShowSignInOn403

from zookeepr.config.environment import load_environment

class SimpleAuthenticator(Authenticator):
    """FIXME: move to model"""
    def check_auth(self, username, password):
        return username == password

def make_app(global_conf, **app_conf):
    """
    Create a WSGI application and return it
    
    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.
    """
    
    # Load our Pylons configuration defaults
    config = load_environment()
    config.init_app(global_conf, app_conf, package='zookeepr')
    
    # Load our default Pylons WSGI app and make g available
    app = pylons.wsgiapp.make_app(config)
    g = app.globals
    
    # YOUR MIDDLEWARE
    # Put your own middleware here, so that any problems are caught by the error
    # handling middleware underneath
    
    # @@@ Change HTTPExceptions to HTTP responses @@@
    app = httpexceptions.make_middleware(app, global_conf)
    
    # security
    app = ShowSignInOn403(app)
    app = Security(app, global_conf=global_conf, http_login=False, cookie_prefix='', login_page='security/signin', logout_page='security/signout', secret=None, authenticator=SimpleAuthenticator)

    # @@@ Error Handling @@@
    app = ErrorHandler(app, global_conf, error_template=error_template, **config.errorware)
    
    # @@@ Static Files in public directory @@@
    staticapp = StaticURLParser(config.paths['static_files'])
    
    # @@@ Cascade @@@ 
    app = Cascade([staticapp, app])
    
    # @@@ Display error documents for 401, 403, 404 status codes (if debug is False also intercepts 500) @@@
    app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)
    
    return app
