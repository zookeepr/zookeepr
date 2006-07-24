from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema
from zookeepr.models import SubmissionType

class SubmissionTypeValidator(schema.Schema):
    name = validators.String()

class NewSubmissionTypeValidator(BaseSchema):
    submissiontype = SubmissionTypeValidator()
    pre_validators = [variabledecode.NestedVariables]


class EditSubmissionTypeValidator(BaseSchema):
    submissiontype = SubmissionTypeValidator()
    pre_validators = [variabledecode.NestedVariables]


class SubmissiontypeController(BaseController, View, Modify):
    validators = {"new" : NewSubmissionTypeValidator(),
                  "edit" : EditSubmissionTypeValidator()}

    model = SubmissionType
    individual = 'submissiontype'
    redirect_map = dict(new=dict(action='index'))
