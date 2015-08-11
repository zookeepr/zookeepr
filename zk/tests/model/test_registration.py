# pytest magic: from .conftest import app_config, db_session

from .fixtures import PersonFactory, RegistrationFactory
from zk.model.registration import Registration
from zk.model.person import Person


class TestRegistration(object):
    """Test the registration model
    """

    def test_person_mapping(self, db_session):
        # person.registration should point to a single registration object
        r = RegistrationFactory()
        p = PersonFactory()
        db_session.flush()

        r.person = p
        db_session.flush()

        p = Person.find_by_id(p.id, abort_404 = False)
        r = Registration.find_by_id(r.id, abort_404 = False)

        # test that p is mapped to r properly
        assert p is not None
        assert r is not None
        assert r == p.registration
        assert p == r.person
