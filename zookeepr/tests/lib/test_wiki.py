from zookeepr.tests import *

from zookeepr.lib import wiki

from paste.fixture import TestApp


class WikiTest(TestBase):
    def setUp(self):
        self.app = TestApp(wiki.get_wiki_response)

    def test_disabled_if_no_moin(self):
        pass

    def test_view(self):
        self.app.get('/wang', status=200)

class RequestZookeeprTest(TestBase):
    def test_setup_args(self):
       pass 
