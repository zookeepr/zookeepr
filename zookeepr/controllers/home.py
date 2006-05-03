from zookeepr.lib.base import *

class HomeController(BaseController):

    def index(self):
        m.subexec('home/index.myt')
