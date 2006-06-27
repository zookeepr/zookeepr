from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import Modify, View
from zookeepr.models import Submission

class SubmissionValidator(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()

class NewSubmissionValidator(schema.Schema):
    submission = SubmissionValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionValidator(schema.Schema):
    submission = SubmissionValidator()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(BaseController, View, Modify):
    validator = {"new" : NewSubmissionValidator(),
                 "edit" : EditSubmissionValidator()}

    model = Submission
    individual = 'submission'
    #conditions = dict(order_by='title')
