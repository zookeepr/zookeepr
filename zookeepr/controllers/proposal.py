from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController, AuthFunc, AuthTrue, AuthFalse, AuthRole
from zookeepr.lib.base import c, g, redirect_to, request, render_response
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, PersonValidator, ProposalTypeValidator, FileUploadValidator
from zookeepr.model import Proposal, ProposalType, Stream, Review, Attachment

class ProposalSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()
    url = validators.String()
    type = ProposalTypeValidator()

class NewProposalSchema(BaseSchema):
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditProposalSchema(BaseSchema):
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]

class StreamValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return g.objectstore.query(Stream).get(value)

class ReviewSchema(schema.Schema):
    familiarity = validators.Int()
    technical = validators.Int()
    experience = validators.Int()
    coolness = validators.Int()
    stream = StreamValidator()
    comment = validators.String()

class NewReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [variabledecode.NestedVariables]

class NewAttachmentSchema(BaseSchema):
    attachment = FileUploadValidator()
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
        c.proposal = g.objectstore.get(Proposal, id)

        review = Review()
        defaults = dict(request.POST)
        errors = {}
        
        if defaults:
            result, errors = NewReviewSchema().validate(defaults)

            if not errors:
                for k in result['review']:
                    setattr(review, k, result['review'][k])

                review.reviewer = c.person
                review.proposal = c.proposal

                g.objectstore.save(review)
                g.objectstore.flush()

                # FIXME: dumb
                redirect_to('/')
                
        c.streams = g.objectstore.query(Stream).select()
        
        good_errors = {}
        for key in errors.keys():
            try:
                for subkey in errors[key].keys():
                    good_errors[key + "." + subkey] = errors[key][subkey]
            except AttributeError:
                good_errors[key] = errors[key]

        return render_response('proposal/review.myt', defaults=defaults, errors=good_errors)
    

    def attach(self, id):
        """Attach a file to the proposal.
        """
        c.proposal = g.objectstore.get(Proposal, id)
        attachment = Attachment()
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = NewAttachmentSchema().validate(defaults)

            if not errors:
                for k in result['attachment']:
                    setattr(attachment, k, result['attachment'][k])
                g.objectstore.save(attachment)
                c.proposal.attachments.append(attachment)

                g.objectstore.flush()

                return redirect_to(action='view', id=id)

        good_errors = {}
        for key in errors.keys():
            try:
                for subkey in errors[key].keys():
                    good_errors[key + "." + subkey] = errors[key][subkey]
            except AttributeError:
                good_errors[key] = errors[key]

        return render_response('proposal/attach.myt', defaults=defaults, errors=good_errors)
