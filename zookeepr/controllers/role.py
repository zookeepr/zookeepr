from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Role

class RoleValidator(schema.Schema):
    name = validators.PlainText()

class NewRoleValidator(BaseSchema):
    role = RoleValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditRoleValidator(BaseSchema):
    role = RoleValidator()
    pre_validators = [variabledecode.NestedVariables]

class RoleController(BaseController, View, Modify):
    schemas = {"new" : NewRoleValidator(),
               "edit" : EditRoleValidator()}

    model = Role
    individual = 'role'
    #conditions = dict(order_by='name')
