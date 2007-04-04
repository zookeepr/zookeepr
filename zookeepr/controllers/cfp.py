import smtplib

from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.validators import BaseSchema, ProposalTypeValidator, FileUploadValidator
from zookeepr.model import Person, ProposalType, Proposal, Attachment
    
class RegistrationSchema(Schema):
    email_address = validators.String(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    fullname = validators.String()

class ProposalSchema(Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    experience = validators.String()
    url = validators.String()
    assistance = validators.Bool()
    
class NewCFPSchema(BaseSchema):
    registration = RegistrationSchema()
    proposal = ProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

class CfpController(SecureController):
    permissions = {'submit': [AuthRole('organiser')]
                   }
    def index(self):
        return render_response("cfp/list.myt")

    def submit(self):
        c.cfptypes = self.dbsession.query(ProposalType).select()

        errors = {}
        defaults = dict(request.POST)

        if request.method == 'POST' and defaults:
            result, errors = NewCFPSchema().validate(defaults, self.dbsession)

            if not errors:
                c.proposal = Proposal()
                # update the objects with the validated form data
                for k in result['proposal']:
                    setattr(c.proposal, k, result['proposal'][k])
                
                c.registration = Person()
                for k in result['registration']:
                    setattr(c.registration, k, result['registration'][k])
                c.registration.proposals.append(c.proposal)

                if result['attachment'] is not None:
                    c.attachment = Attachment()
                    for k in result['attachment']:
                        setattr(c.attachment, k, result['attachment'][k])
                    c.proposal.attachments.append(c.attachment)

                s = smtplib.SMTP(request.environ['paste.config']['app_conf'].get('app_smtp_server'))
                # generate the message from a template
                body = render('cfp/submission_response.myt', id=c.registration.url_hash, fragment=True)
                s.sendmail(request.environ['paste.config']['app_conf'].get('committee_email'),
		    c.registration.email_address, body)
                s.quit()

                return render_response('cfp/thankyou.myt')

        return render_response("cfp/new.myt",
                               defaults=defaults, errors=errors)
