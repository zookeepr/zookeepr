from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Person

class PersonValidator(Schema):
    password = validators.PlainText()
    password_confirm = validators.PlainText()    
    email_address = validators.Email()

    handle = validators.PlainText()
    phone = validators.String()
    fax = validators.String()
    firstname = validators.String()
    lastname = validators.String()

class NewPersonValidator(BaseSchema):
    person = PersonValidator()
    pre_validators = [NestedVariables]

class EditPersonValidator(BaseSchema):
    person = PersonValidator()
    pre_validators = [NestedVariables]

class PersonController(BaseController, View, Modify):
    schemas = {"new" : NewPersonValidator(),
               "edit" : EditPersonValidator()}

    model = Person
    individual = 'person'
    key = 'handle'
