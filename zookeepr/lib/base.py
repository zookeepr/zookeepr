from pylons import Controller, m, h, c, g, session, request, params
import zookeepr.models as model

class BaseController(Controller):
    def __call__(self, action, **params):
        # Insert any code to be run per request here
        Controller.__call__(self, action, **params)