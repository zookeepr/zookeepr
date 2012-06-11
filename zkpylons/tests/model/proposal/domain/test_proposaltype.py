from zkpylons.tests.model import *

class TestProposalTypeModel(CRUDModelTest):
    domain = model.proposal.ProposalType
    samples = [dict(name='example1'),
               dict(name='example2'),
               ]
