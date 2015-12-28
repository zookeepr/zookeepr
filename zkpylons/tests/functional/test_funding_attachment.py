from routes import url_for

from .crud_helper import CrudHelper
from .fixtures import FundingFactory, FundingAttachmentFactory, PersonFactory, RoleFactory

from .utils import do_login


class TestFundingAttachment(CrudHelper):
    def test_permissions(self, app, db_session):
        # Only have view and delete
        # Can't request view, non html response isn't handled properly
        # Any logged in and activated user is good
        CrudHelper.test_permissions(self, app, db_session, good_roles=[], bad_roles=['public'], get_pages=('delete',), post_pages=('delete',))

    def test_new(self):
        # Override CRUD
        pass

    def test_view(self, app, db_session):
        # View returns the attachment as a binary
        user = PersonFactory(roles = [RoleFactory(name = 'organiser')])
        target = FundingAttachmentFactory(filename="bobs.blob", content=bytes("bloblbolbblob"), content_type="custom/blob")
        db_session.commit()

        do_login(app, user)

        resp = app.get(url_for(controller='funding_attachment', action='view', id=target.id))
        assert resp.content_type == "custom/blob"
        assert resp.body == bytes("bloblbolbblob")

    def test_index(self):
        # Override CRUD
        pass

    def test_edit(self):
        # Override CRUD
        pass

    def test_delete(self, app, db_session):
        parent = FundingFactory() # Used for the redirection
        db_session.commit()

        CrudHelper.test_delete(self, app, db_session, target=FundingAttachmentFactory(funding=parent), title="Delete attachment", next_url= url_for(controller='funding', action='view', id=parent.id))

