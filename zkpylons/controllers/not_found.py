from zkpylons.lib.base import *

class NotFoundController(BaseController):
    def view(self):
        """
        This is the last place which is tried during a request to try to find a 
        file to serve.

        The default is just to abort the request with a 404 File not found
        status message.
        """
        c.not_found = True
        return render('/error/404.mako')

