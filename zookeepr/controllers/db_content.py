import logging

from zookeepr.lib.base import *

log = logging.getLogger(__name__)

class DbContentController(BaseController):

    def index(self):
        c.title = "Test"
        c.body = "<p>Hello<br />There</p>"
        return render('/db_content/db_content.myt')
