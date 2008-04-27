import cgi
import types

from formencode.api import Invalid
from pylons import Response, c, g, cache, request, session
import helpers as h
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest, validate
from pylons.templating import render
from pylons.helpers import abort, etag_cache
from pylons.controllers.util import redirect_to
from sqlalchemy.orm import create_session, Query

# the distinction between render and render_response is no longer
# significant as of pylons 0.9.7 or so --Jiri 27.4.2008
from pylons.templating import render as render_response
# on older versions of pylons, use instead:
# from pylons.templating import render_response

from zookeepr import model

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        # Insert any code to be run per request here. The Routes match
        # is under environ['pylons.routes_dict'] should you want to check
        # the action or route vars here

        #default_metadata.connect(
        #    request.environ['paste.config']['app_conf']['dburi']
        #)

        self.dbsession = create_session()

        response = WSGIController.__call__(self, environ, start_response)

        self.dbsession.flush()

        return response
