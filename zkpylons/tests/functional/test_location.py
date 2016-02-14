from .crud_helper import CrudHelper
from .fixtures import LocationFactory

class TestLocation(CrudHelper):
    def test_permissions(self, app, db_session):
        # Special ical page has public permissions
        CrudHelper.test_permissions(self, app, db_session)
        CrudHelper.test_permissions(self, app, db_session, good_roles=['public'], bad_roles=[], get_pages=("ical",), post_pages=[])

    def test_view(self, app, db_session):
        resp = CrudHelper.test_view(self, app, db_session)

        # TODO: parse resp to verify the schedule for the location
