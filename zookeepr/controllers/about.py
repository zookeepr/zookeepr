from zookeepr.lib.base import *

class AboutController(BaseController):
    templates = ["whatson", "programme", "dates",
                 "press", "sydney", "contact",
                 "sponsors"]

    def index(self):
        h.redirect_to(action='whatson')

    def view(self, id):
        if id in self.templates:
            m.subexec("about/%s.myt" % id)
        else:
            raise AttributeError, name
