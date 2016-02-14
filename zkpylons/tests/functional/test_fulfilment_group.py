from routes import url_for

from zk.model import FulfilmentStatus
from .crud_helper import CrudHelper
from .fixtures import FulfilmentStatusFactory, FulfilmentTypeFactory, PersonFactory, FulfilmentGroupFactory

class TestFulfilmentGroup(CrudHelper):
    # Permissions doesn't test pdf page non html response isn't handled properly

    def test_new(self, app, db_session):
        person = PersonFactory()
        db_session.commit()

        data = {
                "person"    : person.id,
                "code"      : "Uncle",
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        target = FulfilmentGroupFactory(person=PersonFactory(firstname="Jim", lastname="Murphy"))
        db_session.commit()
        expected = [target.person.fullname, target.code]
        CrudHelper.test_view(self, app, db_session, target=target, expected=expected, title="Fulfilment Group - %d" % target.id)

    def test_edit(self, app, db_session):
        people = [PersonFactory() for i in range(10)]
        target = FulfilmentGroupFactory(person = people[3])
        db_session.commit()

        initial_values = {
                "person"    : str(target.person.id),
                "code"      : target.code,
                }

        new_values = {
                "person"    : people[5].id,
                "code"      : "Uncle",
               }

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target)

    # TODO: test_pdf
