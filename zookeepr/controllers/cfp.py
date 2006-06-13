from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import *
from zookeepr.lib.validators import Strip

class CFPValidator(Schema):
    email_address = validators.Email()
    password = validators.String()
    password_confirm = validators.String()
    title = validators.String()
    abstract = validators.String()
    url = validators.String()
    attachment = validators.String()
    
class NewCFPValidator(Schema):
    cfp = CFPValidator()
    pre_validators = [Strip("commit"), NestedVariables]

class EditCFPValidator(Schema):
    cfp = CFPValidator()
    pre_validators = [Strip("commit"), NestedVariables]
    
class CfpController(BaseController, View, Modify):
    validator = {
        'new': NewCFPValidator(),
        'edit': EditCFPValidator(),
        }

    model = model.CFP
    individual = 'cfp'

    def submit(self):
        self.new()
