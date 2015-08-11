# pytest magic: from .conftest import app_config, db_session

from .fixtures import PersonFactory
from zk.model.person import Person

class TestPerson(object):
    def test_select_by_url(self, db_session):
        the_hash = "8"*64
        fred = PersonFactory.create(url_hash=the_hash)
        db_session.flush()

        selected = Person.find_by_url_hash(the_hash)

        # one element, a person
        assert type(selected) is Person

        # and it looks like fred
        assert selected == fred
