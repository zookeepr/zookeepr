from zookeepr.lib.base import *

class SubmissionController(BaseController):
    def index(self):
        """List all submissions"""
        m.write("you're listing all submissions")

    def view(self, id):
        """View a submission."""
        m.write("you're viewing submission %s" % id)

    def edit(self, id):
        """Edit a submission."""
        m.write("you're editing submission %s" % id)

    def remove(self, id):
        """Remove a submission"""
        m.write("you're removing submission %s" % id)
