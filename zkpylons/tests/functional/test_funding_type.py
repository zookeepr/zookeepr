from zk.model import FulfilmentStatus
from .crud_helper import CrudHelper
from .fixtures import FundingTypeFactory

class TestFundingType(CrudHelper):
    def test_new(self, app, db_session):
        # Note field can't be set

        data = {
                "name"         : "Typo the shop",
                "active"       : True,
                "notify_email" : "billy@type.org",
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        target = FundingTypeFactory()
        db_session.commit()
        # Note field isn't shown
        expected = [target.name, target.notify_email]
        CrudHelper.test_view(self, app, db_session, target=target, expected=expected)

    def test_index(self, app, db_session):
        types = [FundingTypeFactory() for i in range(10)]
        db_session.commit()
        entries = { s.id : s.name for s in types }

        CrudHelper.test_index(self, app, db_session, entries = entries, title="List Funding Types")

    def test_edit(self, app, db_session):
        target = FundingTypeFactory()
        db_session.commit()

        initial_values = {
                "name"         : target.name,
                "active"       : target.active,
                "notify_email" : target.notify_email,
                }

        new_values = {
                "name"         : "Typo the shop",
                "active"       : True,
                "notify_email" : "billy@type.org",
               }

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target)
