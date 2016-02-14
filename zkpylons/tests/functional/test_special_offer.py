from .crud_helper import CrudHelper
from .fixtures import SpecialOfferFactory

class TestSpecialOffer(CrudHelper):
    def test_view(self, app, db_session):
        resp = CrudHelper.test_view(self, app, db_session)
        # TODO: Also lists all registrations that have used the special offer

    def test_index(self, app, db_session):
        CrudHelper.test_index(self, app, db_session, title="List of special offers")
