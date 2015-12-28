from .crud_helper import CrudHelper

class TestEventType(CrudHelper):
    def test_permissions(self, app, db_session):
        CrudHelper.test_permissions(self, app, db_session, dont_get_pages='view')

    def test_view(self):
        pass # No view page, block crud helper
