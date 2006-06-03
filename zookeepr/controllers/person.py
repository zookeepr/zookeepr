from formencode import validators, compound, schema, variabledecode
from zookeepr.lib.base import *

class PersonValidator(schema.Schema):
    handle = validators.PlainText()
    password = validators.PlainText()
    password_confirm = validators.PlainText()    
    email_address = validators.Email()

class NewPersonValidator(schema.Schema):
    person = PersonValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditPersonValidator(schema.Schema):
    person = PersonValidator()
    pre_validators = [variabledecode.NestedVariables]

class PersonController(BaseController, View, Modify):
    validator = {"new" : NewPersonValidator(),
                 "edit" : EditPersonValidator()}

    model = model.Person
    individual = 'person'
    key = 'handle'
