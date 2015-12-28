from routes import url_for
from BeautifulSoup import BeautifulSoup

from .crud_helper import CrudHelper
from .fixtures import ProposalStatusFactory, ProposalFactory


class TestProposalStatus(CrudHelper):
    def test_view(self, app, db_session):
        target = ProposalStatusFactory()
        props = [ProposalFactory(status = target) for i in range(10)]

        resp = CrudHelper.test_view(self, app, db_session, target=target)

        # View also lists proposals with this status
        soup = BeautifulSoup(resp.body)

        prop_table = soup.find('table')
        rows = prop_table.findAll('tr')

        # 1 row per proposal, 1 heading
        assert len(rows) == len(props) + 1

        del rows[0] # Throw away header

        for i in range(len(rows)):
            # Each row is ordered by id, same as props
            # Each row should contain a link to the proposal view page
            # Each row should contain the title of the proposal
            row_str = str(rows[i])
            prop = props[i]
            assert url_for(controller='proposal', action='view', id=prop.id) in row_str
            assert prop.title in row_str
