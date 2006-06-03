from formencode import validators, compound, schema, variabledecode
from zookeepr.lib.base import *

class RoleValidator(schema.Schema):
    name = validators.PlainText()

class NewRoleValidator(schema.Schema):
    role = RoleValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditRoleValidator(schema.Schema):
    role = RoleValidator()
    pre_validators = [variabledecode.NestedVariables]

class RoleController(BaseController, View, Modify):
    validator = {"new" : NewRoleValidator(),
                 "edit" : EditRoleValidator()}

    model = model.Role
    individual = 'role'
    conditions = dict(order_by='name')
