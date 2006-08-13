from zookeepr.tests.model import *

class TestProposalType(TableTest):
    """Test the ``proposal_type`` table.

    This table stores the list of types that a proposal can be.
    """
    table = 'proposal.tables.proposal_type'
    samples = [dict(name='test'),
               dict(name='test1'),
               ]
    not_nullables = ['name']
    uniques = ['name']
