from zookeepr.lib.base import *

class CfpController(BaseController):
    """Controller for submitting something to the conference"""
    def index(self):
        return h.redirect_to(action='new')

    def view(self, id):
        """View a submission."""
        m.write("you're viewing submission %s" % id)

    def new(self):
        """Create a new submission"""
        c.errors, c.defaults = {}, m.request_args

        c.submissiontypes = model.SubmissionType.select()

        h.log(c.submisiontypes)
        
        if c.defaults:
            # FIXME: flesh out
            h.log(c.defaults)

            # snuh insert
            
            h.redirect_to('profile', id=c.defaults['handle'])
        m.subexec('cfp/new.myt')

    def edit(self, id):
        """Edit a submission."""
        m.write("you're editing submission %s" % id)

    def remove(self, id):
        """Remove a submission"""
        m.write("you're removing submission %s" % id)
