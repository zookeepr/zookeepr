from zookeepr.tests.functional import *
from paste.fixture import AppError

class TestTemplateController(ControllerTest):
    def test_moin_on_404(self):
        resp = self.app.get(url_for(controller='/idontexistlollollol'), status=200)
        resp.mustcontain('/idontexistlollollol?action=edit')
