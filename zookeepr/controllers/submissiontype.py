from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController
from zookeepr.lib.base import BaseController
from zookeepr.lib.generics import Modify, View
from zookeepr.lib.validators import Strip
from zookeepr.models import SubmissionType

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

    model = SubmissionType
    individual = 'submissiontype'
    conditions = dict(order_by='name')
    redirect_map = dict(new=dict(action='index'))
