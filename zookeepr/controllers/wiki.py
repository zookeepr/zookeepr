from zookeepr.lib.base import *

class WikiController(BaseController):
    def view(self, url):
        """
	Get a page from the wiki.
        """
        c.title = url
        return render_response('wiki.myt')
