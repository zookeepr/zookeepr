import cgi
import types

from formencode.api import Invalid
from pylons import Response, c, g, h, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest, validate
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
from sqlalchemy import default_metadata, create_session

from zookeepr import model

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        # Insert any code to be run per request here. The Routes match
        # is under environ['pylons.routes_dict'] should you want to check
        # the action or route vars here
        return WSGIController.__call__(self, environ, start_response)

    def __before__(self, **kwargs):
        """__before__ is run on every request, before passing control
        to the controller. Here we do anything that needs work
        per request."""

        # FIXME - EVIL HACK
        # For some unknown reason _engine disappears
        # So we save it at initialisation and restore it each request
        default_metadata.context._engine = g.engine

        # create a connection to the objectstore that we can use for
        # the life of the request
        g.objectstore = create_session()

        if hasattr(super(BaseController, self), '__before__'):
            return super(BaseController, self).__before__(**kwargs)

    def __after__(self, **kwargs):
        # close the connection to the objectstore
        g.objectstore.close()
        # invalidate it so there's no chance of using it again
        del g.objectstore
