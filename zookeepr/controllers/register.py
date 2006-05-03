from zookeepr.lib.base import *

class RegisterController(BaseController):
    def index(self):
        m.subexec('register/new.myt')
