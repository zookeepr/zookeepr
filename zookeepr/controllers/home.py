from zookeepr.lib.base import *

class HomeController(BaseController):

    def index(self):
        # FIMXE (benno). We need to display something
        # much different if the person is logged in.
        m.subexec('about/index.myt')
