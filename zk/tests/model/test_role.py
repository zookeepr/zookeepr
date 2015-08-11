# pytest magic: from .conftest import app_config, db_session

from .fixtures import PersonFactory, RoleFactory
from zk.model.person import Person
from zk.model.role import Role


class TestRole(object):
    def test_map_person(self, db_session):
        """Test mapping persons to roles"""
        person = PersonFactory()
        role = RoleFactory()
        db_session.flush()

        person.roles.append(role)
        db_session.flush()

        person = Person.find_by_id(person.id, abort_404=False)
        role = Role.find_by_id(role.id, abort_404=False)

        assert role in person.roles
        assert person in role.people
         
    def test_many_roles(self, db_session):
        people = PersonFactory.create_batch(4)
        roles  = RoleFactory.create_batch(2)
        db_session.flush()

        people[0].roles.append(roles[0])
        people[1].roles.append(roles[1])
        people[3].roles.append(roles[1])
        db_session.flush()
        
        p1 = Person.find_by_id(people[0].id, abort_404=False)
        p2 = Person.find_by_id(people[1].id, abort_404=False)
        p3 = Person.find_by_id(people[2].id, abort_404=False)
        p4 = Person.find_by_id(people[3].id, abort_404=False)
        r1 = Role.find_by_id(roles[0].id,    abort_404=False)
        r2 = Role.find_by_id(roles[1].id,    abort_404=False)


        assert r1 in p1.roles
        assert r2 in p2.roles
        assert r2 in p4.roles
        assert len(p3.roles) == 0

        assert r1 not in p2.roles
        assert r1 not in p3.roles
        assert r1 not in p4.roles
        assert r2 not in p1.roles
        assert r2 not in p3.roles
