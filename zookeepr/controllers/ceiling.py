from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, BoundedInt
from zookeepr.model import Ceiling

class CeilingSchema(BaseSchema):
    name = validators.String(not_empty=True)
    max_sold = BoundedInt(min=0)
    available_from = validators.String()
    available_until = validators.String()

class NewCeilingSchema(BaseSchema):
    ceiling = CeilingSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditCeilingSchema(BaseSchema):
    ceiling = CeilingSchema()
    pre_validators = [variabledecode.NestedVariables]

class CeilingController(SecureController, View, Modify):
    schemas = {"new" : NewCeilingSchema(),
               "edit" : EditCeilingSchema()}
    permissions = {"view": [AuthRole('organiser')],
                   "index": [AuthRole('organiser')],
                   "edit": [AuthRole('organiser')],
                   "delete": [AuthRole('organiser')],
                   "new": [AuthRole('organiser')],
                   }

    model = Ceiling
    individual = 'ceiling'
    redirect_map = dict(new=dict(action='index'))
