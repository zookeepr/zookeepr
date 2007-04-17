from zookeepr.lib.base import *

class WikiController(BaseController):
    def view(self, url):
        """
	Get a page from the wiki.
        """
        c.title = url
        return render_response('wiki.myt')
    def view_wiki(self, sfx):
        """
	Get a page from the wiki, using a '/wiki/' prefix; see comments in
	config/routing.py for why we do this...
        """
        c.title = '/wiki/'+sfx
        return render_response('wiki.myt')
