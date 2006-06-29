from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables
from sqlalchemy import create_session

from zookeepr.lib.base import BaseController, c, m
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.models import SubmissionType

class CFPValidator(Schema):
    email_address = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = validators.Int()
    experience = validators.String()
    url = validators.String()
    attachment = validators.String()
    assistance = validators.Bool()
    
class NewCFPValidator(BaseSchema):
    cfp = CFPValidator()
    pre_validators = [NestedVariables]

# FIXME: the edit validator shouldn't exist!
# instead we should probably split the generics up into more granular crud
# and make the test suite only test those that shold be there (or better work
# it out and ensure the ones that shouldn't be here don't work)
class EditCFPValidator(BaseSchema):
    cfp = CFPValidator()
    pre_validators = [NestedVariables]
    
class CfpController(BaseController, View, Modify):
    validators = {
        'new': NewCFPValidator(),
        'edit': EditCFPValidator(),
        }

    #model = CFP
    individual = 'cfp'
    redirect_map = dict(new=dict(action='thankyou'))

    def new(self):
        session = create_session()
        c.cfptypes = session.query(SubmissionType).select()
        session.close()
        Modify.new(self)

    def submit(self):
        self.new()

    def edit(self, id):
        # XXX dirty hack to make tests pass
        session = create_session()
        c.cfptypes = session.query(SubmissionType).select()
        session.close()
        Modify.edit(self, id)

    def thankyou(self):
        m.subexec('cfp/thankyou.myt')
