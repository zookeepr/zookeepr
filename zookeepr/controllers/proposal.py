from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController, AuthFunc, AuthTrue, AuthFalse, AuthRole
from zookeepr.lib.base import c, g, redirect_to, request, render_response
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, PersonValidator, ProposalTypeValidator, FileUploadValidator
from zookeepr.model import Proposal, ProposalType

class ProposalSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()
    url = validators.String()
    type = ProposalTypeValidator()
    attachment = FileUploadValidator()

class NewProposalSchema(BaseSchema):
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditProposalSchema(BaseSchema):
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]

class ProposalController(SecureController, View, Modify):
    model = Proposal
    individual = 'proposal'

    schemas = {"new" : NewProposalSchema(),
               "edit" : EditProposalSchema()}
    permissions = {"edit": [AuthFunc('is_submitter')],
                   "view": [AuthFunc('is_submitter'), AuthRole('reviewer')],
                   "delete": [AuthFunc('is_submitter')],
                   "index": [AuthRole('reviewer')],
                   }

    def __before__(self, **kwargs):
        super(ProposalController, self).__before__(**kwargs)

        c.proposal_types = g.objectstore.query(ProposalType).select()

    def new(self, id):
        self.obj = self.model()
        errors = {}
        defaults = dict(request.POST)
        if defaults:
            result, errors = self.schemas['new'].validate(defaults)

            if not errors:
                for k in result['proposal']:
                    setattr(self.obj, k, result['proposal'][k])

                self.obj.people.append(c.person)

                g.objectstore.save(self.obj)
                g.objectstore.flush()

                redirect_to(action='view', id=self.obj.id)

        c.proposal = self.obj

        good_errors = {}
        for key in errors.keys():
            try:
                for subkey in errors[key].keys():
                    good_errors[key + "." + subkey] = errors[key][subkey]
            except AttributeError:
                good_errors[key] = errors[key]

        return render_response('proposal/new.myt', defaults=defaults, errors=good_errors)

    def is_submitter(self):
        return c.person in self.obj.people

    def review(self, id):
        """Review a proposal.
        """
        return render_response('proposal/review.myt')
    
