from zookeepr.lib.base import *

class HomeController(BaseController):

    def index(self):
        if request.environ.has_key('REMOTE_USER'):
            m.subexec('home.myt')
        else:
            m.subexec('about/index.myt')
