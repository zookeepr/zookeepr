from formencode.variabledecode import variable_decode
from pylons import Controller, m, h, c, g, session, request, params
#import sqlalchemy

import zookeepr.models as model
from zookeepr.lib.generics import *

class BaseController(Controller):
    def __call__(self, action, **params):
        # Insert any code to be run per request here

        # Connect the ORM to the database
        #print "connecting db in Basecontroller.__call__"
        #sqlalchemy.global_connect(g.pylons_config.app_conf['dburi'])
        # clear the objectstore session
        #sqlalchemy.objectstore.clear()

        # Use FormEncode to decode the request args automagically
        if m.request_args:
            m.request_args = variable_decode(m.request_args)

        # Let the base class defer to controller actions
        Controller.__call__(self, action, **params)
