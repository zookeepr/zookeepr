from zookeepr.lib.base import *

class AboutController(BaseController):
    #templates = ["index", "cfp", "contact", "sponsors"]

    def view(self, id):
        #if id in self.templates:
        #    m.subexec("about/%s.myt" % id)
        #else:
        #    m.abort(404, "Object not found")
        m.subexec("about/%s.myt" % id)
