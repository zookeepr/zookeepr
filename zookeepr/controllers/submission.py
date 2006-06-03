from formencode import validators, compound, schema, variabledecode
from zookeepr.lib.base import *

class SubmissionValidator(schema.Schema):
    title = validators.String()

class NewSubmissionValidator(schema.Schema):
    submission = SubmissionValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionValidator(schema.Schema):
    submission = SubmissionValidator()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(BaseController, View, Modify):
    validator = {"new" : NewSubmissionValidator(),
                 "edit" : EditSubmissionValidator()}

    individual = 'submission'
    model = model.Submission
    conditions = dict(order_by='title')
