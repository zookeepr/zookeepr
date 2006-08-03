from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController

class HomeController(SecureController):

    def index(self):
        if c.person:
            resp = render_response('home.myt')
        else:
            resp = render_response('about/index.myt')

        return resp
