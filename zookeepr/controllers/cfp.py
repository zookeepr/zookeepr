from formencode import validators, compound
from formencode.schema import Schema

from zookeepr.lib.base import *

class CFPValidator(Schema):
    pass

class CfpController(BaseController, View, Modify):
    validator = {
        'new': CFPValidator(),
        }

    model = model.CFP
    individual = 'cfp'
