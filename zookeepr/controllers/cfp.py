from zookeepr.lib.base import *

class CfpController(BaseController):
    def index(self):
        m.subexec("cfp/new.myt")
