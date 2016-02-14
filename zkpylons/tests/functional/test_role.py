from routes import url_for
from BeautifulSoup import BeautifulSoup

from .fixtures import CompletePersonFactory, RoleFactory
from .crud_helper import CrudHelper


class TestRole(CrudHelper):
    def test_view(self, app, db_session):
        target = RoleFactory(name='Bob', pretty_name='Ross', display_order=23, comment='Beefcake')
        peeps = [CompletePersonFactory(roles=[target]) for i in range(10)]

        resp = CrudHelper.test_view(self, app, db_session, target=target)

        # View also lists people with the role
        soup = BeautifulSoup(resp.body)
        peeps_table = soup.findAll('table')[1] # Second table

        # 1 row per person, no heading
        assert len(peeps_table.findAll('tr')) == len(peeps)

        # Each person row should contain their fullname, link to their profile, link to their roles
        peeps_table_str = str(peeps_table)
        for p in peeps:
            assert p.fullname in peeps_table_str
            assert url_for(controller='person', action='view', id=p.id) in peeps_table_str
            assert url_for(controller='person', action='roles', id=p.id) in peeps_table_str
            


