from zookeepr.tests.model import *

class TestProposalTypeModel(ModelTest):
    model = 'proposal.ProposalType'
    samples = [dict(name='example1'),
               dict(name='example2'),
               ]
