from zookeepr.lib.base import *

class CfpController(BaseController):
    def index(self):
        """List all submissions"""
        m.write("you're listing all submissions")
        m.write("perhaps you'd like to ")
        m.write('<a href="%s">submit something</a>' % h.url_for(action='new'))

    def view(self, id):
        """View a submission."""
        m.write("you're viewing submission %s" % id)

    def new(self):
        """Create a new submission"""
        m.write("you're creating a new submission")
        errors, defaults = {}, m.request_args
        if defaults:
            # FIXME: flesh out
            m.subexec('thankyou.myt')
        m.subexec('cfp/new.myt', defaults=defaults, errors=errors)

    def edit(self, id):
        """Edit a submission."""
        m.write("you're editing submission %s" % id)

    def remove(self, id):
        """Remove a submission"""
        m.write("you're removing submission %s" % id)
