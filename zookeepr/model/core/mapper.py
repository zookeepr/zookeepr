import datetime
import md5
import random

from sqlalchemy import mapper, relation, MapperExtension, join

from zookeepr.model.submission.tables import *
from zookeepr.model.submission.domain import *

mapper(SubmissionType, submission_type)


mapper(Submission, submission,
       properties = dict(
    submission_type = relation(SubmissionType, lazy=False),
    ))
