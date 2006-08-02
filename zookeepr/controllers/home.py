from zookeepr.lib.base import *

class HomeController(BaseController):

    def index(self):
        if request.environ.has_key('REMOTE_USER'):
            return render_response('home.myt')
        else:
            return render_response('about/index.myt')
