
import logging

from decorator import decorator
from zkpylons.lib.helpers import redirect_to
from pylons.controllers.util import abort
from pylons import request, config
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)

def current_protocol():
    if request.scheme.lower() == 'https':
        return 'https'

    if request.environ.get('HTTPS') in ('on', '1'):
        return 'https'

    if request.environ.get('HTTP_X_FORWARDED_PROTO') == 'https':
        return 'https'

    return 'http'


def ssl_check(ssl_required=[], ssl_allowed=[], ssl_required_all=False, ssl_allowed_all=False):

    if not asbool(config.get('enable_ssl_requirement', False)):
        return

    action = request.environ['pylons.routes_dict']['action']

    if action in ssl_allowed or ssl_allowed_all:             # We don't care if they use http or https
        return
    elif action in ssl_required or ssl_required_all:     # Must have ssl
        protocol = 'https'
    else:
        protocol = 'http'

    if current_protocol() == protocol:
        return

    if request.method.upper() != 'POST':
        log.debug('Redirecting to %s, request: %s', protocol, request.path_info)
        host = config.get('ssl_host')
        if host:
            redirect_to(protocol=protocol, host=host)
        else:
            redirect_to(protocol=protocol)
    else:
        abort(405, headers=[('Allow', 'GET')]) # don't allow POSTs.

def enforce_ssl(required=[], allowed=[], required_all=False, allowed_all=False):
    """
    This is a decorator which can be used to decorate a Pylons controller action.
    It takes the definition of where ssl is required or allowed and passes it
    through to the ssl_check function.
    """
    def enforce(func, self, *args, **kwargs):
        ssl_check(ssl_required=required, ssl_allowed=allowed, ssl_required_all=required_all, ssl_allowed_all=allowed_all)
        return func(self, *args, **kwargs)
    return decorator(enforce)
