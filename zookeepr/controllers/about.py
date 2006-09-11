from zookeepr.lib.auth import SecureController
from zookeepr.lib.base import *

class AboutController(SecureController):
    """Display information about a specific part of the conference.
    """
    def view(self, id):
        """View the information.

        ``view`` is the primary action associated with this controller.
        It does no processing of information, only returns a response
        from the templates.
        """
        return render_response("about/%s.myt" % id)
