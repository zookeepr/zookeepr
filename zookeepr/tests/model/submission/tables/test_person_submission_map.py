from zookeepr.tests.model import *

class TestPersonSubmissionMap(TableTest):
    """Test the ``person_submission_map`` table.

    This table allows us to have an M to N mapping between
    people and their submissions.
    """
    table = 'submission.tables.person_submission_map'
    samples = [dict(id=1, person_id=1, submission_id=1),
                dict(id=2, person_id=2, submission_id=2),
                ]
    not_nullables = ['person_id', 'submission_id']
    uniques = ['id']
