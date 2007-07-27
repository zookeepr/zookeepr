import cgi
import types

from formencode.api import Invalid
from pylons import Response, c, g, h, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest, validate
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
from sqlalchemy import create_session, Query

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
