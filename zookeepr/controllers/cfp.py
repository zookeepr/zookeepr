import sys

from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.mail import *
from zookeepr.lib.validators import BaseSchema, ProposalTypeValidator, FileUploadValidator, AssistanceTypeValidator
from zookeepr.model import ProposalType, Proposal, Attachment, AssistanceType

class CFPModeValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        cfp_mode = request.environ['paste.config']['app_conf'].get('cfp_mode')
        if cfp_mode == 'miniconf' and value['type'].name != 'Miniconf':
            raise Invalid("You can only register miniconfs at this time.", value, state)

class PersonSchema(Schema):
    experience = validators.String()
    bio = validators.String(not_empty=True)
    url = validators.String()

class ProposalSchema(Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    assistance = AssistanceTypeValidator()
    project = validators.String(not_empty=True)
    url = validators.String()
    abstract_video_url = validators.String()

    chained_validators = [CFPModeValidator]

class NewCFPSchema(BaseSchema):
    person = PersonSchema()
    proposal = ProposalSchema()
    #attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

class MiniPersonSchema(Schema):
    experience = validators.String()
    bio = validators.String(not_empty=True)
    #url = validators.String()

class MiniProposalSchema(Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    assistance = AssistanceTypeValidator()
    #project = validators.String(not_empty=True)
    url = validators.String()
    #abstract_video_url = validators.String()

    chained_validators = [CFPModeValidator]

class NewMiniSchema(BaseSchema):
    person = MiniPersonSchema()
    proposal = MiniProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]


class CfpController(SecureController):
    permissions = {'submit': [AuthRole('organiser')]
                  }
    anon_actions = ['index']

    def __init__(self, *args):
        c.cfp_status = request.environ['paste.config']['app_conf'].get('cfp_status')

        # Anyone can submit while the CFP is open
        if c.cfp_status == 'open' and 'submit' in self.permissions:
            del self.permissions['submit']

    def index(self):
        return render_response("cfp/list.myt")

    def submit(self):
        # to close the CFP, change "if 0" to "if 1" :-)
        if 0: 
	    return render_response("cfp/closed.myt")

        c.cfptypes = self.dbsession.query(ProposalType).select()
        c.tatypes = self.dbsession.query(AssistanceType).select()
        c.cfp_mode = request.environ['paste.config']['app_conf'].get('cfp_mode')
        c.signed_in_person = self.dbsession.query(model.Person).get_by(id=session['signed_in_person_id'])
        c.person = c.signed_in_person

        errors = {}
        defaults = dict(request.POST)

        if request.method == 'POST' and defaults:
            result, errors = NewCFPSchema().validate(defaults, self.dbsession)

            if not errors:
                c.proposal = Proposal()
                # update the objects with the validated form data
                for k in result['proposal']:
                    setattr(c.proposal, k, result['proposal'][k])

                c.person.proposals.append(c.proposal)

                for k in result['person']:
                    setattr(c.person, k, result['person'][k])

                #if result['attachment'] is not None:
                #    c.attachment = Attachment()
                #    for k in result['attachment']:
                #        setattr(c.attachment, k, result['attachment'][k])
                #    c.proposal.attachments.append(c.attachment)

                return render_response('cfp/thankyou.myt')

        return render_response("cfp/new.myt",
                               defaults=defaults, errors=errors)

    def submit_mini(self):

        # call-for-miniconfs now closed
        if 1: 
	    return render_response("cfp/closed_mini.myt")

        c.cfptypes = self.dbsession.query(ProposalType).select()
        c.tatypes = self.dbsession.query(AssistanceType).select()
        c.cfp_mode = request.environ['paste.config']['app_conf'].get('cfp_mode')
        c.signed_in_person = self.dbsession.query(model.Person).get_by(id=session['signed_in_person_id'])
        c.person = c.signed_in_person

        errors = {}
        defaults = dict(request.POST)

        if request.method == 'POST' and defaults:
            result, errors = NewMiniSchema().validate(defaults, self.dbsession)

            if not errors:
                c.proposal = Proposal()
                # update the objects with the validated form data
                for k in result['proposal']:
                    setattr(c.proposal, k, result['proposal'][k])

                c.person.proposals.append(c.proposal)

                for k in result['person']:
                    setattr(c.person, k, result['person'][k])

                if result['attachment'] is not None:
                    c.attachment = Attachment()
                    for k in result['attachment']:
                        setattr(c.attachment, k, result['attachment'][k])
                    c.proposal.attachments.append(c.attachment)

                email((c.person.email_address, 
                          'miniconf-props@lists.mel8ourne.org'),
                      render('cfp/thankyou_mini_email.myt', fragment=True))

                return render_response('cfp/thankyou_mini.myt')

        return render_response("cfp/new_mini.myt",
                               defaults=defaults, errors=errors)
