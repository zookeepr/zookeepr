from zookeepr.lib.base import *

class HomeController(BaseController):
    def index(self):
        m.write("this is the home page")
