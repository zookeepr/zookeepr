from .crud_helper import CrudHelper
from .fixtures import StreamFactory

class TestStream(CrudHelper):
    def test_view(self, app, db_session):
        resp = CrudHelper.test_view(self, app, db_session)
        # TODO: Also lists proposals with this status

    def test_index(self, app, db_session):
        CrudHelper.test_index(self, app, db_session, title="List of streams")
