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

class CFPModeValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        cfp_mode = request.environ['paste.config']['app_conf'].get('cfp_mode')
        if cfp_mode == 'miniconf' and value != 'Miniconf':
            raise Invalid("You can only register miniconfs at this time.", value, state)
        elif cfp_mode != 'miniconf' and value == 'Miniconf':
            raise Invalid("You can't register miniconfs at this time.", value, state)

class ProposalSchema(Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    experience = validators.String()
    url = validators.String()
    assistance = validators.Bool()

    chained_validators = [CFPModeValidator]

class NewCFPSchema(BaseSchema):
    registration = RegistrationSchema()
    proposal = ProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

class CfpController(SecureController):
    permissions = {'submit': [AuthRole('organiser')]
                  }

    def __init__(self, *args):
        c.cfp_status = request.environ['paste.config']['app_conf'].get('cfp_status')

        # Anyone can submit while the CFP is open
        if c.cfp_status == 'open' and 'submit' in self.permissions:
            del self.permissions['submit']

    def index(self):
        return render_response("cfp/list.myt")

    def submit(self):
        c.cfptypes = self.dbsession.query(ProposalType).select()
        c.cfp_mode = request.environ['paste.config']['app_conf'].get('cfp_mode')

        errors = {}
        defaults = dict(request.POST)

        if request.method == 'POST' and defaults:
            result, errors = NewCFPSchema().validate(defaults, self.dbsession)

            if not errors:
                c.proposal = Proposal()
                # update the objects with the validated form data
                for k in result['proposal']:
                    setattr(c.proposal, k, result['proposal'][k])

                c.peron = c.signed_in_person
                c.person.registration.proposals.append(c.proposal)

                if result['attachment'] is not None:
                    c.attachment = Attachment()
                    for k in result['attachment']:
                        setattr(c.attachment, k, result['attachment'][k])
                    c.proposal.attachments.append(c.attachment)

                s = smtplib.SMTP(request.environ['paste.config']['app_conf'].get('app_smtp_server'))
                # generate the message from a template
                body = render('cfp/submission_response.myt', id=c.registration.url_hash, fragment=True)
                s.sendmail(request.environ['paste.config']['app_conf'].get('contact_email'), c.registration.email_address, body)
                s.quit()

                return render_response('cfp/thankyou.myt')

        return render_response("cfp/new.myt",
                               defaults=defaults, errors=errors)
