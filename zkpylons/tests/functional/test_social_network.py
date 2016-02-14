from routes import url_for
from BeautifulSoup import BeautifulSoup

from .crud_helper import CrudHelper
from .fixtures import SocialNetworkFactory, CompletePersonFactory

from zk.model import Person, SocialNetwork

class TestSocialNetwork(CrudHelper):
    def test_new(self, app, db_session):
        data = {
                "name"    : "Billy bob's face",
                "logo"    : "your face",
                "url"     : "http://your.face.online/", # Must be of a urlish form
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        target = SocialNetworkFactory()
        peeps = [CompletePersonFactory() for i in range(10)]
        db_session.commit()
        for p in peeps: p.social_networks[target] = "View test peep%i soc net" % p.id

        resp = CrudHelper.test_view(self, app, db_session, target=target)

        # Also lists people who are members of this network
        soup = BeautifulSoup(resp.body)
        person_table = soup.findAll('table')[1] # Second table
        rows = person_table.findAll('tr')

        # 1 row per person in network, 1 heading
        assert len(rows) == len(peeps) + 1
        del rows[0] # Throw away header

        # Rows are sorted by person id
        # Each row must contain:
        #    the person's name
        #    name of their social network
        #    link to their view page
        for i in range(len(peeps)):
            row_str = str(rows[i])
            pers = peeps[i]
            assert pers.fullname in row_str
            assert "View test peep%i soc net" % pers.id in row_str
            assert url_for(controller='person', action='view', id=pers.id) in row_str

    def test_index(self, app, db_session):
        CrudHelper.test_index(self, app, db_session, title="List of Social Networks")

    def test_edit(self, app, db_session):
        target = SocialNetworkFactory()
        db_session.commit()

        new_values = {
                "name"    : "Billy bob's face",
                "logo"    : "your face",
                "url"     : "http://your.face.online/", # Must be of a urlish form
               }

        CrudHelper.test_edit(self, app, db_session, target=target, new_values=new_values)

