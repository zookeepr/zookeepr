from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import SubmissionType

class SubmissionTypeSchema(Schema):
    name = validators.String(not_empty=True)

class NewSubmissionTypeSchema(BaseSchema):
    submissiontype = SubmissionTypeSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionTypeSchema(BaseSchema):
    submissiontype = SubmissionTypeSchema()
    pre_validators = [variabledecode.NestedVariables]

class SubmissiontypeController(SecureController, View, Modify):
    schemas = {"new" : NewSubmissionTypeSchema(),
               "edit" : EditSubmissionTypeSchema()}
    permissions = {"view": [AuthRole('site-admin')],
                   "index": [AuthRole('site-admin')],
                   "edit": [],
                   "delete": [],
                   "new": [],
                   }

    model = SubmissionType
    individual = 'submissiontype'
    redirect_map = dict(new=dict(action='index'))
