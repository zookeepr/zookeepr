import pytest

from .crud_helper import CrudHelper
from .fixtures import TravelFactory, RoleFactory, PersonFactory, CompletePersonFactory

class TestTravel(CrudHelper):
    @pytest.yield_fixture(autouse=True)
    def prep_types(self, db_session):
        # Initial permission check gets very unhappy if reviewer role is missing
        self.user = PersonFactory(roles=[RoleFactory(name='funding_reviewer'), RoleFactory(name='organiser')])
        db_session.commit()
        yield

    def test_permissions(self, app, db_session):
        # Must have BOTH org and funding_reviewer
        CrudHelper.test_permissions(self, app, db_session, good_roles=['organiser', 'funding_reviewer'])
        CrudHelper.test_permissions(self, app, db_session, good_roles=['organiser', 'funding_reviewer'], bad_roles=['organiser'])
        CrudHelper.test_permissions(self, app, db_session, good_roles=['organiser', 'funding_reviewer'], bad_roles=['funding_reviewer'])

    def test_new(self, app, db_session):
        data = {
                # NOTE: No facility to enter the flight details
                "origin_airport" : "Here",
                "destination_airport" : "There",
               }

        CrudHelper.test_new(self, app, db_session, data=data, user=self.user)

    def test_view(self, app, db_session):
        target = TravelFactory(person = CompletePersonFactory())
        db_session.commit()
        # NOTE: No facility to view the flight details
        expected = [target.person.fullname, target.origin_airport, target.destination_airport]
        CrudHelper.test_view(self, app, db_session, target=target, expected=expected, user=self.user)

    def test_index(self, app, db_session):
        groups = [TravelFactory(person=CompletePersonFactory()) for i in range(10)]
        db_session.commit()
        entries = { s.id : [str(s.id), s.person.fullname, s.origin_airport, s.destination_airport] for s in groups }

        CrudHelper.test_index(self, app, db_session, entries = entries, user=self.user)

    def test_edit(self, app, db_session):
        target = TravelFactory()
        db_session.commit()

        initial_values = {
                "origin_airport" : target.origin_airport,
                "destination_airport" : target.destination_airport,
                }

        new_values = {
                # NOTE: No facility to enter the flight details
                "origin_airport" : "Here",
                "destination_airport" : "There",
               }


        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target, user=self.user)

    def test_delete(self, app, db_session):
        CrudHelper.test_delete(self, app, db_session, user=self.user)

