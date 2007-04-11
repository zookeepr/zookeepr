from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole

class AdminController(SecureController):
    """ Miscellaneous admin tasks. """

    permissions = { 'ALL': [AuthRole('organiser')] }

    def test(self):
        """
	Testing, testing, 1, 2, 3.
        """
        return Response("This is a test. Hope you've studied!")
