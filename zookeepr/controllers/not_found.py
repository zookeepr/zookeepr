from zookeepr.lib.base import *

class NotFoundController(BaseController):
    def view(self):
        """
        This is the last place which is tried during a request to try to find a 
        file to serve. It could be used for example to display a template::
        
            def view(self, url):
                return render_response(url+'.myt')
        
        The default is just to abort the request with a 404 File not found
        status message.
        """
        return render_response('not_found.myt')

