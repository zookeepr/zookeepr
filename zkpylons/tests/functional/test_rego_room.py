from .crud_helper import CrudHelper
from .fixtures import RegoRoomFactory, CompletePersonFactory, RegistrationFactory

class TestRegoRoom(CrudHelper):

    def test_new(self, app, db_session):
        peeps = [CompletePersonFactory() for i in range(10)]
        regos = [RegistrationFactory() for i in range(10)]
        db_session.commit()

        # TODO: Again, we are specifying ids by hand - it's nuts
        data = {
                "rego" : regos[2].id,
                "room" : "42 down the left",
                "by"   : peeps[0].id,
               }

        CrudHelper.test_new(self, app, db_session, data=data, title="Add a new room")

    def test_view(self, app, db_session):
        target = RegoRoomFactory()
        db_session.commit()
        expected = [target.rego.person.fullname, target.room, target.by.fullname]
        CrudHelper.test_view(self, app, db_session, target=target, expected=expected, title="Viewing room number")

    def test_index(self, app, db_session):
        groups = [RegoRoomFactory() for i in range(10)]
        db_session.commit()
        entries = { s.id : [str(s.id), s.by.fullname, s.rego.person.fullname, s.room] for s in groups }

        CrudHelper.test_index(self, app, db_session, entries = entries, title="List of Room numbers")

    def test_edit(self, app, db_session):
        peeps = [CompletePersonFactory() for i in range(10)]
        regos = [RegistrationFactory() for i in range(10)]
        target = RegoRoomFactory()
        db_session.commit()

        initial_values = {
                "rego" : str(target.rego.id),
                "room" : target.room,
                "by"   : str(target.by.id),
                }

        new_values = {
                "rego" : regos[2].id,
                "room" : "42 down the left",
                "by"   : peeps[0].id,
               }


        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target)

