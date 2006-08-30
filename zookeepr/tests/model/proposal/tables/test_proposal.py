import StringIO

from zookeepr.tests.model import *

class TestProposal(TableTest):
    """Test the ``proposal`` table.

    This table stores proposals made by candidate speakers.
    """
    table = model.proposal.tables.proposal
    samples = [dict(title='Test Paper',
                    abstract='Test Abstract',
                    experience='None at all',
                    url='gopher://',
                    proposal_type_id=1,
                    attachment=buffer("attachment"), #StringIO.StringIO("attachment"),
                    assistance=True,
                    ),
               dict(title='Test BOF',
                    abstract='some bof',
                    experience='Some',
                    url="sqlite:////somedb.db",
                    proposal_type_id=2,
                    attachment=buffer("snuh"), #StringIO.StringIO("snuh"),
                    assistance=False,
                    ),
               ]
