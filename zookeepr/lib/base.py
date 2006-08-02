import cgi
import types

from formencode.api import Invalid
from pylons import Response, c, g, h, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest, validate
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
from sqlalchemy import default_metadata, create_session

import zookeepr.models as model

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        # Insert any code to be run per request here. The Routes match
        # is under environ['pylons.routes_dict'] should you want to check
        # the action or route vars here
        return WSGIController.__call__(self, environ, start_response)

    def __before__(self, **kwargs):
        """__before__ is run on every requet, before passing control
        to the controller. Here we do anything that needs work
        per request."""
        action = kwargs["action"]

        # FIXME - EVIL HACK
        # For some unknown reason _engine disappears
        # So we save it at initialisation and restore it each request
        default_metadata.context._engine = model.evil_jf

        # Convert the request_args into something sane. Basically what
        # I am doing here is finding anything encoded as FieldStorage
        # rather than a plain string and then encoding it as either a
        # a string, or a file
        request_args = dict(request.POST)
        if request_args:
            for key in request_args:
                if isinstance(request_args[key], cgi.FieldStorage):
                    if request_args[key].file and \
                           type(request_args[key].file) == types.FileType:
                        request_args[key] = request_args[key].value
                    else:
                        request_args[key] = request_args[key].value


        # Create a connection to the object store that we can use for the
        # life of the request.
        self.objectstore = create_session()

    def __after__(self, **kwargs):
        # Close the connection to the objectstore
        self.objectstore.close()
        # and invalidate it so there's no chance of using it incorrectly
        self.objectstore = None
