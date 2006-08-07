from sqlalchemy import mapper, relation

from zookeepr.model.core import Person
from zookeepr.model.submission.tables import submission, submission_type, person_submission_map
from zookeepr.model.submission.domain import Submission, SubmissionType

# Map the SubmissionType object onto the submision_type table
mapper(SubmissionType, submission_type)

# Map the Submission object onto the submission table
mapper(Submission, submission,
    properties = {
        'type': relation(SubmissionType, lazy=False),
        'people': relation(Person, secondary=person_submission_map,
            backref='submissions')
    }
    )
