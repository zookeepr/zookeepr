
import logging

from pylons.controllers.util import abort, redirect_to
from pylons import request, config
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)

def current_protocol():
    if request.scheme.lower() == 'https':
        return 'http'

    if request.environ.get('HTTPS') == 'on':
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
        redirect_to(protocol=protocol)
    else:
        abort(405, headers=[('Allow', 'GET')]) # don't allow POSTs.


