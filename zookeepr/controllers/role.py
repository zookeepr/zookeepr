from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Role

class RoleSchema(Schema):
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
    permissions = {"new": [],
                   "view": [],
                   "edit": [],
                   "delete": [],
                   "index": [],
                   }

    model = Role
    individual = 'role'
    #conditions = dict(order_by='name')
