from sqlalchemy import mapper

from zookeepr.model.submission.tables import submission, submission_type
from zookeepr.model.submission.domain import Submission, SubmissionType

# Map the SubmissionType object onto the submision_type table
mapper(SubmissionType, submission_type)

# Map the Submission object onto the submission table
mapper(Submission, submission)
