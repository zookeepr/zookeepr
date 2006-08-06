from zookeepr.tests.model.table import *

class TestSubmissionType(TableTest):
    """Test the ``submission_type`` table.

    This table stores the list of types that a submission can be.
    """
    table = 'submission.tables.submission_type'
    samples = [dict(name='test'),
               dict(name='test1'),
               ]
    not_nullables = ['name']
    uniques = ['name']
