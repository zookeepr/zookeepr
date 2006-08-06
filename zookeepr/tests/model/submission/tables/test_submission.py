import StringIO

from zookeepr.tests.model.table import *

class TestSubmission(TableTest):
    """Test the ``submission`` table.

    This table stores submissions made by candidate speakers.
    """
    table = 'submission.tables.submission'
    samples = [dict(title='Test Paper',
                    abstract='Test Abstract',
                    experience='None at all',
                    url='gopher://',
                    submission_type_id=1,
                    person_id=1,
                    attachment=buffer("attachment"), #StringIO.StringIO("attachment"),
                    assistance=True,
                    ),
               dict(title='Test BOF',
                    abstract='some bof',
                    experience='Some',
                    url="sqlite:////somedb.db",
                    submission_type_id=2,
                    person_id=37,
                    attachment=buffer("snuh"), #StringIO.StringIO("snuh"),
                    assistance=False,
                    ),
               ]
