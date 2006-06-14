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

# FIXME: the edit validator shouldn't exist!
# instead we should probably split the generics up into more granular crud
# and make the test suite only test those that shold be there (or better work
# it out and ensure the ones that shouldn't be here don't work)
class EditCFPValidator(Schema):
    cfp = CFPValidator()
    pre_validators = [Strip("commit"), NestedVariables]
    
class CfpController(BaseController, View, Modify):
    validator = {
        # FIXME: The automagic test looks for the 'new' action, so map
        # that as well as 'submit', which only calls new()
        'new': NewCFPValidator(),
        'submit': NewCFPValidator(),
        'edit': EditCFPValidator(),
        }

    model = model.CFP
    individual = 'cfp'

    def submit(self):
        self.new()
