from formencode.variabledecode import variable_decode
from pylons import Controller, m, h, c, g, session, request, params

from sqlalchemy import create_engine

import zookeepr.models as model
from zookeepr.lib.generics import *

class BaseController(Controller):
    def __before__(self, **kwargs):
        # Insert any code to be run per request here

        
        # Connect the ORM to the database
        eng = create_engine(g.pylons_config.app_conf['dburi'])
        model.metadata.connect(eng)
        
        # Use FormEncode to decode the request args automagically
        if m.request_args:
            m.request_args = variable_decode(m.request_args)
