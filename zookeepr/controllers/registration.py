from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Create
from zookeepr.lib.validators import BaseSchema

class NewRegistrationSchema(BaseSchema):
    pass

class RegistrationController(BaseController, Create):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               }
