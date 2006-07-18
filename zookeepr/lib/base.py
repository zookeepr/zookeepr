import cgi
import types

from formencode.api import Invalid
from pylons import Controller, m, h, c, g, session, request

from sqlalchemy import default_metadata

import zookeepr.models as model

class BaseController(Controller):

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
        if m.request_args:
            for key in m.request_args:
                if isinstance(m.request_args[key], cgi.FieldStorage):
                    if m.request_args[key].file and \
                           type(m.request_args[key].file) == types.FileType:
                        m.request_args[key] = m.request_args[key].value
                    else:
                        m.request_args[key] = m.request_args[key].value
