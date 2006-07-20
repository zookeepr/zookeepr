import smtplib

from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables
from sqlalchemy import create_session

from zookeepr.lib.base import BaseController, c, m, request, h
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.models import SubmissionType, Submission, Registration

class RegistrationValidator(Schema):
    email_address = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)

class SubmissionValidator(Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = validators.Int()
    experience = validators.String()
    url = validators.String()
    attachment = validators.String()
    assistance = validators.Bool()
    
class NewCFPValidator(BaseSchema):
    registration = RegistrationValidator()
    submission = SubmissionValidator()
    pre_validators = [NestedVariables]

class CfpController(BaseController):

    def submit(self):
        session = create_session()
        c.cfptypes = session.query(SubmissionType).select()

        errors = {}
        defaults = m.request_args

        new_reg = Registration()
        new_sub = Submission()
        
        if request.method == 'POST' and defaults:
            result, errors = NewCFPValidator().validate(defaults)

            if not errors:
                # update the objects with the validated form data
                for k in result['submission']:
                    setattr(new_sub, k, result['submission'][k])
                for k in result['registration']:
                    setattr(new_reg, k, result['registration'][k])

                session.save(new_reg)
                session.save(new_sub)

                new_reg.submissions.append(new_sub)
                
                session.flush()
                session.close()

                #s = smtplib.SMTP("localhost")
                #s.sendmail(new_reg.email_address, "lca2007", "hi!")
                #s.quit()
                
                return h.redirect_to(action='thankyou')

        c.registration = new_reg
        c.submission = new_sub
        
        session.close()

        # unmangle the errors
        good_errors = {}
        for key in errors.keys():
            for subkey in errors[key].keys():
                good_errors[key + "." + subkey] = errors[key][subkey]

        m.subexec("cfp/new.myt", defaults=defaults, errors=good_errors)

    def thankyou(self):
        m.subexec('cfp/thankyou.myt')
