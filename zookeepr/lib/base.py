import cgi
import types
from formencode.api import Invalid
from pylons import Controller, m, h, c, g, session, request, params

from sqlalchemy import create_engine

import zookeepr.models as model

class BaseController(Controller):

    def __before__(self, **kwargs):
        """__before__ is run on every requet, before passing control
        to the controller. Here we do anything that needs work
        per request."""
        action = kwargs["action"]

        # Connect the ORM to the database
        eng = create_engine(g.pylons_config.app_conf['dburi'])
        model.metadata.connect(eng)

        # Convert the request_args into something sane. Basically what
        # I am doing here is finding anything encoded as FieldStorage
        # rather than a plain string and then encoding it as either a
        # a string, or a file
        if m.request_args:
            for key in m.request_args:
                if isinstance(m.request_args[key], cgi.FieldStorage):
                    if m.request_args[key].file and \
                           type(m.request_args[key].file) == types.FileType:
                        m.request_args[key] = m.request_args[key].file
                    else:
                        m.request_args[key] = m.request_args[key].value
