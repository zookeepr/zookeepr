import logging
import zookeepr.lib.helpers as h
from pylons import request, response, session, tmpl_context as c

from zookeepr.model import meta

from zookeepr.lib.base import BaseController, render

log = logging.getLogger(__name__)

# Provide a sitemap for the Zookeepr controlled content.
class SitemapController(BaseController):

    def view(self):
        return render('/sitemap.mako')
