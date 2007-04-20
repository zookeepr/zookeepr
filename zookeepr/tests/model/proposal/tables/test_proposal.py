from zookeepr.tests.model import *

class TestProposalTable(TableTest):
    """Test the ``proposal`` table.

    This table stores proposals made by candidate speakers.
    """
    table = model.proposal.tables.proposal
    samples = [dict(title='Test Paper',
                    abstract='Test Abstract',
                    url='gopher://',
                    proposal_type_id=1,
                    assistance_type_id=1,
                    ),
               dict(title='Test BOF',
                    abstract='some bof',
                    url="sqlite:////somedb.db",
                    proposal_type_id=2,
                    assistance_type_id=2,
                    ),
               ]
