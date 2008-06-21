from formencode import validators, compound, schema, variabledecode, Invalid
from paste.deploy.converters import asbool

from zookeepr.lib.auth import SecureController, AuthFunc, AuthTrue, AuthFalse, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.mail import *
from zookeepr.lib.crud import Update, View
from zookeepr.lib.validators import BaseSchema, ProposalTypeValidator, PersonValidator, FileUploadValidator, AssistanceTypeValidator, EmailAddress, NotExistingPersonValidator, StreamValidator, ReviewSchema
from zookeepr.model import Proposal, ProposalType, Stream, Review, Attachment, AssistanceType, Role, Person
from zookeepr.controllers.person import PersonSchema

import random

from zookeepr.config.lca_info import lca_info

class NewPersonSchema(PersonSchema):
    experience = validators.String(not_empty=True)
    bio = validators.String(not_empty=True)
    url = validators.String()
    mobile = validators.String(not_empty=True)

class ExistingPersonSchema(schema.Schema):
    experience = validators.String(not_empty=True)
    bio = validators.String(not_empty=True)
    url = validators.String()
    mobile = validators.String(not_empty=True)

class ProposalSchema(schema.Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    assistance = AssistanceTypeValidator()
    project = validators.String()
    url = validators.String()
    abstract_video_url = validators.String()

class MiniProposalSchema(BaseSchema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    url = validators.String()

class NewProposalSchema(BaseSchema):
    person = NewPersonSchema()
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]

class ExistingProposalSchema(BaseSchema):
    person = ExistingPersonSchema()
    proposal = ProposalSchema()
    pre_validators = [variabledecode.NestedVariables]

class NewMiniProposalSchema(BaseSchema):
    person = NewPersonSchema()
    proposal = MiniProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [variabledecode.NestedVariables]

class ExistingMiniProposalSchema(BaseSchema):
    person = ExistingPersonSchema()
    proposal = MiniProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [variabledecode.NestedVariables]

class NotYetReviewedValidator(validators.FancyValidator):
    """Make sure the reviewer hasn't yet reviewed this proposal"""

    messages = {
        "already": "You've already reviewed this proposal, try editing the existing review."
        }

    def validate_python(self, value, state):
        review = state.query(Review).filter_by(reviewer_id=c.signed_in_person.id, proposal_id=c.proposal.id).first()
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

class ProposalController(SecureController, View, Update):
    model = Proposal
    individual = 'proposal'

    schemas = {"new" : NewProposalSchema(),
               "edit" : ExistingProposalSchema(),
               "new_mini" : NewMiniProposalSchema(),
               "edit_mini" : ExistingMiniProposalSchema()}

    permissions = {"new": [AuthFalse()],
                   "edit": [AuthFunc('is_submitter'), AuthRole('organiser')],
                   "view": [AuthFunc('is_submitter'), AuthRole('reviewer'),
                                                        AuthRole('organiser')],
                   "summary": [AuthRole('organiser'), AuthRole('reviewer')],
                   "delete": [AuthFunc('is_submitter')],
                   "review": [AuthRole('reviewer'), AuthRole('organiser')],
                   "attach": [AuthRole('organiser')],
                   "review_index": [AuthRole('reviewer')], 
                   "talk": True,
                   "index": [AuthTrue()],
                   "submit": True,
                   "submit_mini": True,
                   }

    def __init__(self, *args):
        c.cfp_status = lca_info['cfp_status']
        c.cfmini_status = lca_info['cfmini_status']

    def __before__(self, **kwargs):
        super(ProposalController, self).__before__(**kwargs)

        c.proposal_types = self.dbsession.query(ProposalType).all()
        c.assistance_types = self.dbsession.query(AssistanceType).all()

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
        collection = self.dbsession.query(model.Proposal).from_statement("""
                            SELECT *
                            FROM review AS r
                            LEFT JOIN proposal AS p ON(p.id=r.proposal_id)
                            WHERE p.proposal_type_id IN(1,3)
                            GROUP BY r.proposal_id
                            HAVING COUNT(r.proposal_id) < (
                                    (SELECT COUNT(id) FROM review) /
                                    (SELECT COUNT(id) FROM proposal WHERE proposal_type_id IN(1,3)) + 1)
                            ORDER BY RANDOM()""")
        for proposal in collection:
            #print proposal.id
            if not [ r for r in proposal.reviews if r.reviewer == c.signed_in_person ] and proposal.id != id:
                c.next_review_id = proposal.id
                break
        else:
            # somehow didn't find one, so pick one at random
            # (the collection is shuffled, so item 0 is random enough)
            c.next_review_id = 1



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

        c.streams = self.dbsession.query(Stream).all()

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

    def talk(self, id):
        if c.proposal.accepted:
            return render_response('proposal/talk.myt')
        else:
            return redirect_to('/programme')

    def edit(self, id):
        c.person = c.proposal.people[0];
        c.cfptypes = self.dbsession.query(ProposalType).all()
        c.tatypes = self.dbsession.query(AssistanceType).all()

        errors = {}
        defaults = dict(request.POST)

        if defaults:
            if c.proposal.type.name == 'Miniconf':
                result, errors = self.schemas['edit_mini'].validate(defaults, self.dbsession)
            else:
                result, errors = self.schemas['edit'].validate(defaults, self.dbsession)

            if errors:
                if asbool(request.environ['paste.config']['global_conf'].get('debug')):
                    warnings.warn("edit: form validation failed: %s" % errors)
            else:
                # update the object with the posted data
                for k in result[self.individual]:
                    setattr(self.obj, k, result[self.individual][k])

                for k in result['person']:
                    setattr(c.person, k, result['person'][k])

                self.dbsession.update(self.obj)
                self.dbsession.flush()

                # call postflush hook
                self._edit_postflush()

                default_redirect = dict(action='view', id=self.identifier(self.obj))
                return render_response('proposal/edit_thankyou.myt')

        # call the template
        return render_response('%s/edit.myt' % self.individual, defaults=defaults, errors=errors)

    def review_index(self):
        c.person = c.signed_in_person
        # hack for bug#34, don't show miniconfs to reviewers
        # Jiri: unless they're also organisers...
        if 'organiser' in [r.name for r in c.signed_in_person.roles]:
            c.proposal_types = self.dbsession.query(ProposalType).all()
        else:
            c.proposal_types = self.dbsession.query(ProposalType).filter(ProposalType.c.name <> 'Miniconf').all()

        c.assistance_types = self.dbsession.query(AssistanceType).all()

        c.num_proposals = 0
        reviewer_role = self.dbsession.query(Role).filter(Role.c.name == 'reviewer').all()
        c.num_reviewers = len(reviewer_role[0].people)
        for pt in c.proposal_types:
            stuff = self.dbsession.query(Proposal).filter(Proposal.c.proposal_type_id==pt.id).all()
            c.num_proposals += len(stuff)
            setattr(c, '%s_collection' % pt.name, stuff)
        for at in c.assistance_types:
            stuff = self.dbsession.query(Proposal).filter(Proposal.c.assistance_type_id==at.id).all()
            setattr(c, '%s_collection' % at.name, stuff)


        return super(ProposalController, self).index()

    def summary(self):

        if 'reviewer' not in [r.name for r in c.signed_in_person.roles]:
            c.proposal_types = self.dbsession.query(ProposalType).all()
        else:
            c.proposal_types = self.dbsession.query(ProposalType).filter(ProposalType.c.name <> 'Miniconf').all()

        c.assistance_types = self.dbsession.query(AssistanceType).all()

        for pt in c.proposal_types:
            stuff = self.dbsession.query(Proposal).filter(Proposal.c.proposal_type_id==pt.id).all()
            stuff.sort(self.score_sort)
            setattr(c, '%s_collection' % pt.name, stuff)
        for at in c.assistance_types:
            stuff = self.dbsession.query(Proposal).filter(Proposal.c.assistance_type_id==at.id).all()
            setattr(c, '%s_collection' % at.name, stuff)

        return render_response('proposal/summary.myt')

    def score_sort(self, proposal1, proposal2):
        return cmp(self.review_avg_score(proposal2), self.review_avg_score(proposal1))

    def review_avg_score(self,proposal):
        total_score = 0
        num_reviewers = 0
        for review in proposal.reviews:
            if review.score is not None:
                num_reviewers += 1
                total_score += review.score
        if num_reviewers == 0:
            return 0
        return total_score*1.0/num_reviewers

    def index(self):
        if self.logged_in():
            c.person = c.signed_in_person
            return super(ProposalController, self).index()
        else:
            abort(403)

    def submit(self):
        # if call for papers has closed:
        if c.cfp_status == 'closed':
           return render_response("proposal/closed.myt")
        elif c.cfp_status == 'not_open':
           return render_response("proposal/not_open.myt")
        else:
            c.cfptypes = self.dbsession.query(ProposalType).all()
            c.tatypes = self.dbsession.query(AssistanceType).all()

            errors = {}
            defaults = dict(request.POST)

            if request.method == 'POST' and defaults:
                if c.signed_in_person:
                    schema = self.schemas['edit']
                else:
                    schema = self.schemas['new']

                result, errors = schema().validate(defaults, self.dbsession)
                if not errors:
                    c.proposal = Proposal()
                    # update the objects with the validated form data
                    for k in result['proposal']:
                        setattr(c.proposal, k, result['proposal'][k])

                    if not c.signed_in_person:
                        c.person = model.Person()
                        for k in result['person']:
                            setattr(c.person, k, result['person'][k])
                        self.dbsession.save(c.person)
                    else:
                        c.person = c.signed_in_person
                        for k in result['person']:
                            setattr(c.person, k, result['person'][k])

                    c.person.proposals.append(c.proposal)

                    #if result['attachment'] is not None:
                    #    c.attachment = Attachment()
                    #    for k in result['attachment']:
                    #        setattr(c.attachment, k, result['attachment'][k])
                    #    c.proposal.attachments.append(c.attachment)

                    return render_response('proposal/thankyou.myt')

        return render_response("proposal/new.myt",
                               defaults=defaults, errors=errors)

    def submit_mini(self):

        # call-for-miniconfs now closed
        if c.cfmini_status == 'closed':
            return render_response("proposal/closed_mini.myt")
        elif c.cfmini_status == 'not_open':
            return render_response("proposal/not_open_mini.myt")
        else:
            c.cfptypes = self.dbsession.query(ProposalType).all()
            c.tatypes = self.dbsession.query(AssistanceType).all()

            errors = {}
            defaults = dict(request.POST)

            if request.method == 'POST' and defaults:
                if c.signed_in_person:
                    schema = ExistingMiniProposalSchema
                else:
                    schema = NewMiniProposalSchema
                result, errors = schema().validate(defaults, self.dbsession)

                if not errors:
                    c.proposal = Proposal()
                    # update the objects with the validated form data
                    for k in result['proposal']:
                        setattr(c.proposal, k, result['proposal'][k])

                    if not c.signed_in_person:
                        c.person = model.Person()
                        for k in results['person']:
                            setattr(c.person, k, results['person'][k])
                        self.dbsession.save(c.person)
                    else:
                        c.person = c.signed_in_person
                        for k in result['person']:
                            setattr(c.person, k, result['person'][k])

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
                          render('proposal/thankyou_mini_email.myt', fragment=True))

                    return render_response('proposal/thankyou_mini.myt')

            return render_response("proposal/new_mini.myt",
                                   defaults=defaults, errors=errors)
