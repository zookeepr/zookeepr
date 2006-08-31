from zookeepr.tests.model import *

class TestProposalTypeModel(ModelTest):
    domain = model.proposal.ProposalType
    samples = [dict(name='example1'),
               dict(name='example2'),
               ]
