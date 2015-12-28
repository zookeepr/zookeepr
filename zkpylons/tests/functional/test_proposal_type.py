from .crud_helper import CrudHelper
from .fixtures import ProposalTypeFactory

class TestProposalType(CrudHelper):
    def test_view(self, app, db_session):
        target = ProposalTypeFactory(notify_email="joe@blogs.wordpress.com")
        CrudHelper.test_view(self, app, db_session, target=target)

    def test_edit(self, app, db_session):
        target = ProposalTypeFactory(notify_email="joe@blogs.wordpress.com")
        CrudHelper.test_edit(self, app, db_session, target=target)

