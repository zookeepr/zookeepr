from formencode import validators, compound, schema, variabledecode, Invalid

from zookeepr.lib.auth import SecureController, AuthFunc, AuthTrue, AuthFalse, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, PersonValidator, ProposalTypeValidator, FileUploadValidator, StreamValidator, ReviewSchema, AssistanceTypeValidator
from zookeepr.model import Proposal, ProposalType, Stream, Review, Attachment, AssistanceType, Role
import random

class ProposalSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    url = validators.String()
    type = ProposalTypeValidator()
    assistance = AssistanceTypeValidator()

class NewProposalSchema(BaseSchema):
    ignore_key_missing = True
    proposal = ProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditProposalSchema(BaseSchema):
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]


class NotYetReviewedValidator(validators.FancyValidator):
    """Make sure the reviewer hasn't yet reviewed this proposal"""

    messages = {
        "already": "You've already reviewed this proposal, try editing the existing review."
        }
    
    def validate_python(self, value, state):
        review = state.query(Review).get_by(reviewer_id=c.signed_in_person.id, proposal_id=c.proposal.id)
        if review is not None:
            raise Invalid(self.message('already', None),
                          value, state)
        

class NewReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [variabledecode.NestedVariables]
    chained_validators = [NotYetReviewedValidator()]

class NewAttachmentSchema(BaseSchema):
    attachment = FileUploadValidator()
    pre_validators = [variabledecode.NestedVariables]

class ProposalController(SecureController, View, Modify):
    model = Proposal
    individual = 'proposal'

    schemas = {"new" : NewProposalSchema(),
               "edit" : EditProposalSchema()}
    permissions = {"edit": [AuthFunc('is_submitter'), AuthRole('organiser')],
                   "view": [AuthFunc('is_submitter'), AuthRole('reviewer')],
                   "summary": [AuthRole('organiser'), AuthRole('reviewer')],
                   "delete": [AuthFunc('is_submitter')],
                   "index": [AuthRole('reviewer')],
                   }

    def __before__(self, **kwargs):
        super(ProposalController, self).__before__(**kwargs)

        c.proposal_types = self.dbsession.query(ProposalType).select()
        c.assistance_types = self.dbsession.query(AssistanceType).select()

    def new(self, id):
        errors = {}
        defaults = dict(request.POST)
        if defaults:
            result, errors = self.schemas['new'].validate(defaults, self.dbsession)

            if not errors:
                c.proposal = self.obj = self.model()
                for k in result['proposal']:
                    setattr(c.proposal, k, result['proposal'][k])
                self.obj.people.append(c.signed_in_person)
                self.dbsession.save(c.proposal)
                if result.has_key('attachment') and result['attachment'] is not None:
                    att = Attachment()
                    for k in result['attachment']:
                        setattr(att, k, result['attachment'][k])
                    self.obj.attachments.append(att)
                    self.dbsession.save(att)
                
                self.dbsession.flush()

                redirect_to(action='view', id=self.obj.id)

        return render_response('proposal/new.myt', defaults=defaults, errors=errors)

    def is_submitter(self):
        return c.signed_in_person in self.obj.people

    def review(self, id):
        """Review a proposal.
        """
        c.proposal = self.dbsession.query(model.Proposal).get(id)

        defaults = dict(request.POST)
        errors = {}

        # Next ID for skipping
        collection = self.dbsession.query(self.model).select_by(Proposal.c.proposal_type_id == 1)
        random.shuffle(collection)
        min_reviews = 100
        for p in collection:
            if len(p.reviews) < min_reviews:
                min_reviews = len(p.reviews)
            elif not p.reviews:
                min_reviews = 0
        for proposal in collection:
            print proposal.id
            if not [ r for r in proposal.reviews if r.reviewer == c.signed_in_person ] and (not proposal.reviews or len(proposal.reviews) <= min_reviews) and proposal.id != id:
                c.next_review_id = proposal.id
                break



        if defaults:
            result, errors = NewReviewSchema().validate(defaults, self.dbsession)

            if not errors:
                review = Review()
                for k in result['review']:
                    setattr(review, k, result['review'][k])

                self.dbsession.save(review)

                review.reviewer = c.signed_in_person
                c.proposal.reviews.append(review)

                self.dbsession.flush()

                if c.next_review_id:
                    return redirect_to(action='review', id=c.next_review_id)

                return redirect_to(action='index')

        c.streams = self.dbsession.query(Stream).select()

        return render_response('proposal/review.myt', defaults=defaults, errors=errors)


    def attach(self, id):
        """Attach a file to the proposal.
        """
        c.proposal = self.dbsession.query(Proposal).get(id)
        defaults = dict(request.POST)
        errors = {}

        if defaults:
            result, errors = NewAttachmentSchema().validate(defaults, self.dbsession)

            if not errors:
                attachment = Attachment()
                for k in result['attachment']:
                    setattr(attachment, k, result['attachment'][k])
                c.proposal.attachments.append(attachment)

                self.dbsession.flush()

                return redirect_to(action='view', id=id)

        return render_response('proposal/attach.myt', defaults=defaults, errors=errors)

    def view(self):
        # save the current proposal id so we can refer to it later when we need to
        # bounce back here from other controllers
        # crazy shit with RUDBase means id is on self.obj
        session['proposal_id'] = self.obj.id
        session.save()
        return super(ProposalController, self).view()

    def edit(self, id):
        c.person = self.dbsession.get(model.Person, session['signed_in_person_id'])
        return super(ProposalController, self).edit(id)


    def index(self):
        c.person = self.dbsession.get(model.Person, session['signed_in_person_id'])
        # hack for bug#34, don't show miniconfs to reviewers
        if 'reviewer' not in [r.name for r in c.signed_in_person.roles]:
            c.proposal_types = self.dbsession.query(ProposalType).select()
        else:
            c.proposal_types = self.dbsession.query(ProposalType).select_by(ProposalType.c.name <> 'Miniconf')

        c.assistance_types = self.dbsession.query(AssistanceType).select()

        c.num_proposals = 5
        reviewer_role = self.dbsession.query(Role).select_by(Role.c.name == 'reviewer')
        c.num_reviewers = len(reviewer_role[0].people)
        for pt in c.proposal_types:
            stuff = self.dbsession.query(Proposal).select_by(Proposal.c.proposal_type_id==pt.id)
            c.num_proposals += len(stuff)
            setattr(c, '%s_collection' % pt.name, stuff)
        for at in c.assistance_types:
            stuff = self.dbsession.query(Proposal).select_by(Proposal.c.assistance_type_id==at.id)
            setattr(c, '%s_collection' % at.name, stuff)
       

        return super(ProposalController, self).index()


    def summary(self):

        if 'reviewer' not in [r.name for r in c.signed_in_person.roles]:
            c.proposal_types = self.dbsession.query(ProposalType).select()
        else:
            c.proposal_types = self.dbsession.query(ProposalType).select_by(ProposalType.c.name <> 'Miniconf')

        c.assistance_types = self.dbsession.query(AssistanceType).select()

        for pt in c.proposal_types:
            stuff = self.dbsession.query(Proposal).select_by(Proposal.c.proposal_type_id==pt.id)
            stuff.sort(self.score_sort)
            setattr(c, '%s_collection' % pt.name, stuff)
        for at in c.assistance_types:
            stuff = self.dbsession.query(Proposal).select_by(Proposal.c.assistance_type_id==at.id)
            setattr(c, '%s_collection' % at.name, stuff)

        return render_response('proposal/summary.myt')

    def score_sort(self, proposal1, proposal2):
        return self.review_avg_score(proposal2) - self.review_avg_score(proposal1)

    def review_avg_score(self,proposal):
        total_score = 0
        num_reviewers = 0
        for review in proposal.reviews:
            num_reviewers += 1
            total_score += review.score
        if num_reviewers == 0:
            return 0
        return total_score/num_reviewers


