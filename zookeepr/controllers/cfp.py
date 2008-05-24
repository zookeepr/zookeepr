import sys

from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.mail import *
from zookeepr.lib.validators import BaseSchema, ProposalTypeValidator, FileUploadValidator, AssistanceTypeValidator
from zookeepr.model import ProposalType, Proposal, Attachment, AssistanceType

from zookeepr.config.lca_info import lca_info

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

class NewMiniSchema(BaseSchema):
    person = MiniPersonSchema()
    proposal = MiniProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]


class CfpController(SecureController):
    #permissions removed since submit* displays appropirate template file upon closed/not_open settings.
    permissions = {}
    anon_actions = ['index', 'submit', 'submit_mini']

    def __init__(self, *args):
        c.cfp_status = lca_info['cfp_status']
        c.cfmini_status = lca_info['cfmini_status']


        # When the CFP status is closed or not open we allow anonymous requests to the submit() action which responds appropriately with a nice message. 
        #if c.cfp_status == 'closed' or c.cfp_status == 'not_open':
        #    self.anon_actions.append('submit')
        #if c.cfmini_status == 'closed' or c.cfmini_status == 'not_open':
        #    self.anon_actions.append('submit_mini')

    def index(self):
        return render_response("cfp/list.myt")

    def submit(self):
        # if call for papers has closed:
        if c.cfp_status == 'closed':
           return render_response("cfp/closed.myt")
        elif c.cfp_status == 'not_open':
           return render_response("cfp/not_open.myt")
        elif self.logged_in() is False:
           return render_response("cfp/log_in.myt")
        else:
            c.cfptypes = self.dbsession.query(ProposalType).select()
            c.tatypes = self.dbsession.query(AssistanceType).select()
            c.signed_in_person = self.dbsession.query(model.Person).filter_by(id=session['signed_in_person_id']).one()
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
        if c.cfmini_status == 'closed':
            return render_response("cfp/closed_mini.myt")
        elif c.cfmini_status == 'not_open':
            return render_response("cfp/not_open_mini.myt")
        elif self.logged_in() is False:
            return render_response("cfp/mini_log_in.myt")
        else:
            c.cfptypes = self.dbsession.query(ProposalType).select()
            c.tatypes = self.dbsession.query(AssistanceType).select()
            c.signed_in_person = self.dbsession.query(model.Person).filter_by(id=session['signed_in_person_id']).one()
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
                              lca_info['mini_conf_email']),
                          render('cfp/thankyou_mini_email.myt', fragment=True))

                    return render_response('cfp/thankyou_mini.myt')

            return render_response("cfp/new_mini.myt",
                                   defaults=defaults, errors=errors)
