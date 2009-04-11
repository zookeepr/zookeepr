import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, FileUploadValidator, PersonSchema, AssistanceTypeValidator, ProposalTypeValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Proposal, ProposalType, AssistanceType, Attachment, Stream, Review, Role, AccommodationAssistanceType, TravelAssistanceType

from zookeepr.lib.validators import ReviewSchema

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)


class NewPersonSchema(BaseSchema):
    allow_extra_fields = False

    experience = validators.String(not_empty=True)
    bio = validators.String(not_empty=True)
    url = validators.String()
    mobile = validators.String(not_empty=True)

class ExistingPersonSchema(BaseSchema):
    allow_extra_fields = False

    experience = validators.String(not_empty=True)
    bio = validators.String(not_empty=True)
    url = validators.String()
    mobile = validators.String(not_empty=True)

class ProposalSchema(BaseSchema):
    allow_extra_fields = False

    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    audience = TargetAudienceValidator()
    accommodation_assistance = AccommodationAssistanceTypeValidator()
    travel_assistance = TravelAssistanceTypeValidator()
    project = validators.String()
    url = validators.String()
    abstract_video_url = validators.String()
    video_release = validators.Bool()
    slides_release = validators.Bool()

#class MiniProposalSchema(BaseSchema):
#    allow_extra_fields = False
#    title = validators.String(not_empty=True)
#    abstract = validators.String(not_empty=True)
#    type = ProposalTypeValidator()
#    audience = TargetAudienceValidator()
#    url = validators.String()
#

class NewProposalSchema(BaseSchema):
    person = NewPersonSchema()
    proposal = ProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

class ExistingProposalSchema(BaseSchema):
    person = ExistingPersonSchema()
    proposal = ProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

#class NewMiniProposalSchema(BaseSchema):
#    person = NewPersonSchema()
#    proposal = MiniProposalSchema()
#    attachment = FileUploadValidator()
#    pre_validators = [variabledecode.NestedVariables]
#
#class ExistingMiniProposalSchema(BaseSchema):
#    person = ExistingPersonSchema()
#    proposal = MiniProposalSchema()
#    attachment = FileUploadValidator()
#    pre_validators = [variabledecode.NestedVariables]
#

class NewReviewSchema(BaseSchema):
    pre_validators = [NestedVariables]

    review = ReviewSchema()

class NewAttachmentSchema(BaseSchema):
    attachment = FileUploadValidator(not_empty=True)
    pre_validators = [NestedVariables]

class ProposalController(BaseController):

    def __init__(self, *args):
        c.cfp_status = lca_info['cfp_status']
        c.cfmini_status = lca_info['cfmini_status']
        c.paper_editing = lca_info['paper_editing']

    def __before__(self, **kwargs):
        c.proposal_types = ProposalType.find_all()
        c.assistance_types = AssistanceType.find_all()
        c.target_audiences = TargetAudience.find_all()
        c.accommodation_assistance_types = AccommodationAssistanceType.find_all()
        c.travel_assistance_types = TravelAssistanceType.find_all()


    @dispatch_on(POST="_new")
    def new(self):
        if c.cfp_status == 'closed':
           return render("proposal/closed.mako")
        elif c.cfp_status == 'not_open':
           return render("proposal/not_open.mako")

        c.person = h.signed_in_person()

        return render("proposal/new.mako")

    @validate(schema=NewProposalSchema(), form='new', post_only=False, on_get=True, variable_decode=True)
    def _new(self):

        person_results = self.form_result['person']
        proposal_results = self.form_result['proposal']
        attachment_results = self.form_result['attachment']

        c.proposal = Proposal(**proposal_results)
        c.proposal.status = ProposalStatus.find_by_name('Pending')
        meta.Session.add(c.proposal)

        if not h.signed_in_person():
            c.person = model.Person(**person_results)
            meta.Session.add(c.person)
            email(c.person.email_address, render('/person/new_person_email.mako'))
        else:
            c.person = h.signed_in_person()
            for key in person_results:
                setattr(c.person, key, self.form_result['person'][key])

        c.person.proposals.append(c.proposal)

        if attachment_results is not None:
            c.attachment = Attachment(**attachment_results)
            c.proposal.attachments.append(c.attachment)
            meta.Session.add(c.attachment)

        meta.Session.commit()
        email(c.person.email_address, render('proposal/thankyou_email.mako'))

        return render('proposal/thankyou.mako')

    @dispatch_on(POST="_review")
    @authorize(h.auth.has_reviewer_role)
    def review(self, id):
        c.streams = Stream.find_all()
        c.proposal = Proposal.find_by_id(id)
        if c.proposal is None:
            abort(404, "No such object")

        return render('proposal/review.mako')

    @validate(schema=NewReviewSchema(), form='review', post_only=False, on_get=True, variable_decode=True)
    @authorize(h.auth.has_reviewer_role)
    def _review(self, id):
        """Review a proposal.
        """
        c.proposal = Proposal.find_by_id(id)
        if c.proposal is None:
            abort(404, "No such object")


        # Move to model
        next = meta.Session.query(Proposal).from_statement("""
              SELECT
                  p.id
              FROM
                  (SELECT id
                   FROM proposal
                   WHERE id <> %d
                     AND proposal_type_id = %d
                   EXCEPT
                       SELECT proposal_id AS id
                       FROM review
                       WHERE review.reviewer_id <> %d) AS p
              LEFT JOIN
                      review AS r
                              ON(p.id=r.proposal_id)
              GROUP BY
                      p.id
              ORDER BY COUNT(r.reviewer_id), RANDOM()
              LIMIT 1
        """ % (c.proposal.id, c.proposal.type.id, c.signed_in_person.id))
        next = next.first()
        if next is not None:
            c.next_review_id = next.id
            c.reviewed_everything = False
        else:
            # looks like you've reviewed everything!
            c.next_review_id = None
            c.reviewed_everything = True

        person = h.signed_in_person()
        if person in [ review.reviewer for review in proposal.reviews]:
            h.flash('Already reviewed')
            return redirect_to(action='review', id=c.next_review_id)

        results = self.form_result['review']
        review = Review(**results)

        meta.Session.add(review)
        c.proposal.reviews.append(review)

        review.reviewer = person

        meta.Session.commit()

        if c.next_review_id:
            return redirect_to(action='review', id=c.next_review_id)

        h.flash("No more papers to review")

        return redirect_to('/proposal/review_index')



    @authorize(h.auth.is_valid_user)
    @dispatch_on(POST="_attach")
    def attach(self, id):
        return render('proposal/attach.mako')


    @validate(schema=NewAttachmentSchema(), form='attach', post_only=False, on_get=True)
    def _attach(self, id):
        """Attach a file to the proposal.
        """
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)
        if c.proposal is None:
            abort(404, "No such object")

        person_results = self.form_result['attachment']
        attachment = Attachment(**person_results)

        c.proposal.attachments.append(attachment)

        meta.Session.commit()

        h.flash("File was attached")

        return redirect_to(action='view', id=id)


    @authorize(h.auth.is_valid_user)
    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_submitter(id), h.auth.has_organiser_role, h.auth.has_reviewer_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)
        if c.proposal is None:
            abort(404, "No such object")

        return render('proposal/view.mako')

    @dispatch_on(POST="_new")
    @authorize(h.auth.is_valid_user)
    def edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)
        if c.proposal is None:
            abort(404, "No such object")

        c.person = c.proposal.people[0]
        for person in c.proposal.people:
            if h.signed_in_person() == person:
                c.person = person

        defaults = h.object_to_defaults(c.proposal, 'proposal')
        defaults.update(h.object_to_defaults(c.person, 'person'))
        # This is horrible, don't know a better way to do it
        if c.proposal.type:
            defaults['proposal.type'] = defaults['proposal.proposal_type_id']
        if c.proposal.travel_assistance:
            defaults['proposal.travel_assistance'] = defaults['proposal.travel_assistance_type_id']
        if c.proposal.travel_assistance:
            defaults['proposal.accommodation_assistance'] = defaults['proposal.accommodation_assistance_type_id']
        if c.proposal.travel_assistance:
            defaults['proposal.accommodation_assistance'] = defaults['proposal.accommodation_assistance_type_id']


        form = render('/proposal/edit.mako')
        return htmlfill.render(form, defaults)


    @validate(schema=ExistingProposalSchema(), form='edit', post_only=False, on_get=True, variable_decode=True)
    @authorize(h.auth.is_valid_user)
    def _edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)
        if c.proposal is None:
            abort(404, "No such object")


        for key in self.form_result['person']:
            setattr(c.person, key, self.form_result['person'][key])

        for key in self.form_result['proposal']:
            setattr(c.person, key, self.form_result['proposal'][key])

        meta.Session.commit()

        if lca_info['proposal_update_email'] != '':
            body = "Subject: LCA Proposal Updated\n\nid: %d\nTitle: %s\nURL: %s" % (c.proposal.id, c.proposal.title, "http://" + h.host_name() + h.url_for(action="view"))
            email(lca_info['proposal_update_email'], body)

        return render('proposal/edit_thankyou.mako')

    @authorize(h.auth.has_reviewer_role)
    def review_index(self):
        c.person = h.signed_in_person()
        c.num_proposals = 0
        reviewer_role = Role.find_by_name('reviewer')
        c.num_reviewers = len(reviewer_role.people)
        for pt in c.proposal_types:
            stuff = Proposal.find_all_by_proposal_type_id(pt.id)
            c.num_proposals += len(stuff)
            setattr(c, '%s_collection' % pt.name, stuff)
        for aat in c.accommodation_assistance_types:
            stuff = Proposal.find_by_accommodation_assistance_type_id(aat.id)
            setattr(c, '%s_collection' % aat.name, stuff)
        for tat in c.travel_assistance_types:
            stuff = Proposal.find_by_travel_assistance_type_id(tat.id)
            setattr(c, '%s_collection' % tat.name, stuff)

        return render('proposal/list_review.mako')

    @authorize(h.auth.has_reviewer_role)
    def summary(self):
        for pt in c.proposal_types:
            stuff = Proposal.find_all_by_proposal_type_id(pt.id)
            stuff.sort(self._score_sort)
            setattr(c, '%s_collection' % pt.name, stuff)
        for aat in c.accommodation_assistance_types:
            stuff = Proposal.find_by_accommodation_assistance_type_id(aat.id)
            setattr(c, '%s_collection' % aat.name, stuff)
        for tat in c.travel_assistance_types:
            stuff = Proposal.find_by_travel_assistance_type_id(tat.id)
            setattr(c, '%s_collection' % tat.name, stuff)

        return render('proposal/summary.mako')

    def _score_sort(self, proposal1, proposal2):
        return cmp(self._review_avg_score(proposal2), self._review_avg_score(proposal1))

    def _review_avg_score(self,proposal):
        total_score = 0
        num_reviewers = 0
        for review in proposal.reviews:
            if review.score is not None:
                num_reviewers += 1
                total_score += review.score
        if num_reviewers == 0:
            return 0
        return total_score*1.0/num_reviewers

    @authorize(h.auth.is_valid_user)
    def index(self):
        c.person = h.signed_in_person()
        return render('/proposal/list.mako')

# FIXME move to its own controller
#    @dispatch_on(POST="_new")
#    def submit_mini(self):
#        # call for miniconfs has closed
#        if c.cfmini_status == 'closed':
#            return render("proposal/closed_mini.mako")
#        elif c.cfmini_status == 'not_open':
#            return render("proposal/not_open_mini.mako")
#
#        return render("proposal/new_mini.mako")
#
#    @validate(schema=NewProposalSchema(), form='new', post_only=False, on_get=True, variable_decode=True)
#    def _submit_mini(self):
#        else:
#            c.cfptypes = self.dbsession.query(ProposalType).all()
#            c.tatypes = self.dbsession.query(AssistanceType).all()
#
#            errors = {}
#            defaults = dict(request.POST)
#
#            if request.method == 'POST' and defaults:
#                if c.signed_in_person:
#                    schema = self.schemas['mini_edit']
#                else:
#                    schema = self.schemas['mini_new']
#
#                result, errors = schema().validate(defaults, self.dbsession)
#                if not errors:
#                    c.proposal = Proposal()
#                    # update the objects with the validated form data
#                    for k in result['proposal']:
#                        setattr(c.proposal, k, result['proposal'][k])
#
#                    if not c.signed_in_person:
#                        c.person = model.Person()
#                        for k in result['person']:
#                            setattr(c.person, k, result['person'][k])
#                        self.dbsession.save(c.person)
#                        email(c.person.email_address,
#                            render('person/new_person_email.myt', fragment=True))
#                    else:
#                        c.person = c.signed_in_person
#                        for k in result['person']:
#                            setattr(c.person, k, result['person'][k])
#
#                    c.person.proposals.append(c.proposal)
#
#                    for k in result['person']:
#                        setattr(c.person, k, result['person'][k])
#
#                    if result['attachment'] is not None:
#                        c.attachment = Attachment()
#                        for k in result['attachment']:
#                            setattr(c.attachment, k, result['attachment'][k])
#                        c.proposal.attachments.append(c.attachment)
#
#                    return render_response('proposal/thankyou_mini.myt')

    @authorize([h.auth.has_reviewer_role, h.auth.has_organiser_role])
    def approve(self):
        defaults = dict(request.POST)

        c.highlight = set()

        if request.method == 'POST' and defaults:
            for proposal, status in defaults.items():
                if proposal == 'Commit' or status=='-':
                    continue
                assert proposal.startswith('talk.')
                proposal = int(proposal[5:])
                c.highlight.add(proposal)
                proposal = Proposal.find_by_id(proposal)
                status = ProposalStatus.find_by_name(status)
                proposal.status = status

        c.proposals = self.dbsession.query(Proposal).all()
        c.statuses = self.dbsession.query(ProposalStatus).all()
        return render("proposal/approve.mako")
