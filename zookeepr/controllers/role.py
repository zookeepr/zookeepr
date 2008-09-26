from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Role

class RoleSchema(BaseSchema):
    name = validators.PlainText()

class NewRoleSchema(BaseSchema):
    role = RoleSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditRoleSchema(BaseSchema):
    role = RoleSchema()
    pre_validators = [variabledecode.NestedVariables]

class RoleController(SecureController, View, Modify):
    schemas = {"new" : NewRoleSchema(),
               "edit" : EditRoleSchema()}
    permissions = {"new": [AuthRole('organiser')],
                   "view": [AuthRole('organiser')],
                   "edit": [AuthRole('organiser')],
                   "delete": [AuthRole('organiser')],
                   "index": [AuthRole('organiser')],
                   }

    model = Role
    individual = 'role'
