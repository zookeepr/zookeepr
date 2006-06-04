from formencode import validators, compound, schema, variabledecode
from zookeepr.lib.base import *

class Strip:
    def __init__(self, *args):
        self.to_strip = args

    def to_python(self, value_dict, state):
        for strip in self.to_strip:
            if strip in value_dict:
                del value_dict[strip]
        return value_dict

class PersonValidator(schema.Schema):
    password = validators.PlainText()
    password_confirm = validators.PlainText()    
    email_address = validators.Email()

    handle = validators.PlainText()
    phone = validators.String()
    fax = validators.String()
    firstname = validators.String()
    lastname = validators.String()

class NewPersonValidator(schema.Schema):
    person = PersonValidator()
    pre_validators = [Strip("commit"), variabledecode.NestedVariables]

class EditPersonValidator(schema.Schema):
    person = PersonValidator()
    pre_validators = [variabledecode.NestedVariables]

class PersonController(BaseController, View, Modify):
    validator = {"new" : NewPersonValidator(),
                 "edit" : EditPersonValidator()}

    model = model.Person
    individual = 'person'
    key = 'handle'
