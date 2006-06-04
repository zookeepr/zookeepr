from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController
from zookeepr.lib.base import *
from zookeepr.lib.validators import Strip

class SubmissionTypeValidator(schema.Schema):
    name = validators.String()

class NewSubmissionTypeValidator(schema.Schema):
    submissiontype = SubmissionTypeValidator()
    pre_validators = [Strip("commit"), variabledecode.NestedVariables]


class EditSubmissionTypeValidator(schema.Schema):
    submissiontype = SubmissionTypeValidator()
    pre_validators = [Strip('commit'), variabledecode.NestedVariables]


class SubmissiontypeController(BaseController, SecureController, View, Modify):
    validator = {"new" : NewSubmissionTypeValidator(),
                 "edit" : EditSubmissionTypeValidator()}

    model = model.SubmissionType
    individual = 'submissiontype'
    conditions = dict(order_by='name')
