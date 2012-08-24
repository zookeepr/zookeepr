import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, PersonValidator, ProposalValidator, FileUploadValidator, PersonSchema, ProposalTypeValidator, TargetAudienceValidator, ProposalStatusValidator, AccommodationAssistanceTypeValidator, TravelAssistanceTypeValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Proposal, ProposalType, ProposalStatus, TargetAudience, Attachment, Stream, Review, Role, AccommodationAssistanceType, TravelAssistanceType, Person

from zkpylons.lib.validators import ReviewSchema

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class NewPersonSchema(BaseSchema):
    allow_extra_fields = False

    experience = validators.String(not_empty=True)
    bio = validators.String(not_empty=True)
    url = validators.URL(add_http=True, check_exists=False, not_empty=False)
    mobile = validators.String(not_empty=True)

class ExistingPersonSchema(BaseSchema):
    allow_extra_fields = False

    experience = validators.String(not_empty=True)
    bio = validators.String(not_empty=True)
    url = validators.URL(add_http=True, check_exists=False, not_empty=False)
    mobile = validators.String(not_empty=True)

class ProposalSchema(BaseSchema):
    allow_extra_fields = False

    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    private_abstract = validators.String()
    technical_requirements = validators.String(not_empty=False)
    type = ProposalTypeValidator()
    audience = TargetAudienceValidator()
    accommodation_assistance = AccommodationAssistanceTypeValidator()
    travel_assistance = TravelAssistanceTypeValidator()
    project = validators.String()
    url = validators.URL(add_http=True, check_exists=False, not_empty=False)
    abstract_video_url = validators.URL(add_http=True, check_exists=False, not_empty=False)
    video_release = validators.Bool()
    slides_release = validators.Bool()

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
    person_to_edit = PersonValidator()

class NewEditReviewSchema(BaseSchema):
    pre_validators = [NestedVariables]
    review = ReviewSchema()

class NewAttachmentSchema(BaseSchema):
    attachment = FileUploadValidator(not_empty=True)
    pre_validators = [NestedVariables]

class ApproveSchema(BaseSchema):
    talk = ForEach(ProposalValidator())
    status = ForEach(ProposalStatusValidator())

class ProposalController(BaseController):

    def __init__(self, *args):
        c.cfp_status = lca_info['cfp_status']
        c.cfmini_status = lca_info['cfmini_status']
        c.proposal_editing = lca_info['proposal_editing']
        c.cfp_hide_assistance_info = lca_info['cfp_hide_assistance_info']
        c.cfp_hide_scores = lca_info['cfp_hide_scores']

    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        c.proposal_types = ProposalType.find_all()
        c.target_audiences = TargetAudience.find_all()
        c.accommodation_assistance_types = AccommodationAssistanceType.find_all()
        c.travel_assistance_types = TravelAssistanceType.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        if c.cfp_status == 'closed':
           if not h.auth.authorized(h.auth.Or(h.auth.has_organiser_role, h.auth.has_late_submitter_role)):
              return render("proposal/closed.mako")
        elif c.cfp_status == 'not_open':
           return render("proposal/not_open.mako")

        c.person = h.signed_in_person()
        h.check_for_incomplete_profile(c.person)

        defaults = {
            'proposal.type': 1,
            'proposal.video_release': 1,
            'proposal.slides_release': 1,
            'proposal.travel_assistance' : 1,
            'proposal.accommodation_assistance' : 1,
            'person.name': c.person.firstname + " " + c.person.lastname,
            'person.mobile': c.person.mobile,
            'person.experience': c.person.experience,
            'person.bio': c.person.bio,
            'person.url': c.person.url,
        }
        defaults['person_to_edit'] = c.person.id
        defaults['name'] = c.person.firstname + " " + c.person.lastname
        form = render("proposal/new.mako")
        return htmlfill.render(form, defaults)

    @validate(schema=NewProposalSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        if c.cfp_status == 'closed':
           if not h.auth.authorized(h.auth.Or(h.auth.has_organiser_role, h.auth.has_late_submitter_role)):
              return render("proposal/closed.mako")
        elif c.cfp_status == 'not_open':
           return render("proposal/not_open.mako")

        person_results = self.form_result['person']
        proposal_results = self.form_result['proposal']
        attachment_results = self.form_result['attachment']

        proposal_results['status'] = ProposalStatus.find_by_name('Pending')

        c.proposal = Proposal(**proposal_results)
        c.proposal.abstract = self.clean_abstract(c.proposal.abstract)
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
            attachment = Attachment(**attachment_results)
            c.proposal.attachments.append(attachment)
            meta.Session.add(attachment)

        meta.Session.commit()
        email(c.person.email_address, render('proposal/thankyou_email.mako'))

        h.flash("Proposal submitted!")
        return redirect_to(controller='proposal', action="index", id=None)

    @dispatch_on(POST="_review")
    @authorize(h.auth.has_reviewer_role)
    def review(self, id):
        c.streams = Stream.select_values()
        c.proposal = Proposal.find_by_id(id)
        c.signed_in_person = h.signed_in_person()
        c.next_review_id = Proposal.find_next_proposal(c.proposal.id, c.proposal.type.id, c.signed_in_person.id)

        c.review = Review.find_by_proposal_reviewer(id, c.signed_in_person.id, abort_404=False)
        if c.review:
            c.form = 'edit'
            defaults = h.object_to_defaults(c.review, 'review')
            if c.review.score == None:
                defaults['review.score'] = ''
            if c.review.stream_id:
                defaults['review.stream'] = c.review.stream_id

            form = render('/review/edit.mako')
            return htmlfill.render(form, defaults)
        else:
            c.form = 'new'
            return render('/review/new.mako')

    @validate(schema=NewEditReviewSchema(), form='review', post_only=True, on_get=True, variable_decode=True)
    @authorize(h.auth.has_reviewer_role)
    def _review(self, id):
        """Review a proposal.
        """
        c.proposal = Proposal.find_by_id(id)
        c.signed_in_person = h.signed_in_person()
        c.next_review_id = Proposal.find_next_proposal(c.proposal.id, c.proposal.type.id, c.signed_in_person.id)

        c.review = Review.find_by_proposal_reviewer(id, c.signed_in_person.id, abort_404=False)
        if c.review:
            for key in self.form_result['review']:
                setattr(c.review, key, self.form_result['review'][key])

            # update the objects with the validated form data
            meta.Session.commit()
            h.flash("Review Updated Successfully")
            return redirect_to(controller='review', action='view', id=c.review.id)

        else:
            results = self.form_result['review']
            review = Review(**results)

            meta.Session.add(review)
            review.proposal = c.proposal
            review.reviewer = c.signed_in_person

            meta.Session.commit()
            h.flash("Review Added Successfully")

        if c.next_review_id:
            return redirect_to(action='review', id=c.next_review_id)

        h.flash("No more proposals to review")

        return redirect_to(action='review_index')

    @dispatch_on(POST="_attach")
    def attach(self, id):
        return render('proposal/attach.mako')


    @validate(schema=NewAttachmentSchema(), form='attach', post_only=True, on_get=True, variable_decode=True)
    def _attach(self, id):
        """Attach a file to the proposal.
        """
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)

        attachment_results = self.form_result['attachment']
        attachment = Attachment(**attachment_results)

        c.proposal.attachments.append(attachment)

        meta.Session.commit()

        h.flash("File was attached")

        return redirect_to(action='view', id=id)

    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_submitter(id), h.auth.has_organiser_role, h.auth.has_reviewer_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)

        return render('proposal/view.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        if not h.auth.authorized(h.auth.has_organiser_role):
            if c.proposal_editing == 'closed' and not h.auth.authorized(h.auth.has_late_submitter_role):
                return render("proposal/editing_closed.mako")
            elif c.proposal_editing == 'not_open':
                return render("proposal/editing_not_open.mako")

        c.proposal = Proposal.find_by_id(id)

        c.person = c.proposal.people[0]
        for person in c.proposal.people:
            if h.signed_in_person() == person:
                c.person = person

        defaults = h.object_to_defaults(c.proposal, 'proposal')
        defaults.update(h.object_to_defaults(c.person, 'person'))
        defaults['person.name'] = c.person.firstname + " " + c.person.lastname
        # This is horrible, don't know a better way to do it
        if c.proposal.type:
            defaults['proposal.type'] = defaults['proposal.proposal_type_id']
        if c.proposal.travel_assistance:
            defaults['proposal.travel_assistance'] = defaults['proposal.travel_assistance_type_id']
        if c.proposal.accommodation_assistance:
            defaults['proposal.accommodation_assistance'] = defaults['proposal.accommodation_assistance_type_id']
        if c.proposal.audience:
            defaults['proposal.audience'] = defaults['proposal.target_audience_id']

        defaults['person_to_edit'] = c.person.id
        defaults['name'] = c.person.firstname + " " + c.person.lastname
        c.miniconf = (c.proposal.type.name == 'Miniconf')
        form = render('/proposal/edit.mako')
        return htmlfill.render(form, defaults)


    @validate(schema=ExistingProposalSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        if not h.auth.authorized(h.auth.has_organiser_role):
            if c.proposal_editing == 'closed' and not h.auth.authorized(h.auth.has_late_submitter_role):
                return render("proposal/editing_closed.mako")
            elif c.proposal_editing == 'not_open':
                return render("proposal/editing_not_open.mako")

        c.proposal = Proposal.find_by_id(id)
        for key in self.form_result['proposal']:
            setattr(c.proposal, key, self.form_result['proposal'][key])

        c.proposal.abstract = self.clean_abstract(c.proposal.abstract)

        c.person = self.form_result['person_to_edit']
        if (c.person.id == h.signed_in_person().id or
                             h.auth.authorized(h.auth.has_organiser_role)):
            for key in self.form_result['person']:
                setattr(c.person, key, self.form_result['person'][key])
            p_edit = "and author"
        else:
            p_edit = "(but not author)"

        meta.Session.commit()

        if lca_info['proposal_update_email'] != '':
            body = "Subject: %s Proposal Updated\n\nID:    %d\nTitle: %s\nType:  %s\nURL:   %s" % (h.lca_info['event_name'], c.proposal.id, c.proposal.title, c.proposal.type.name.lower(), "http://" + h.host_name() + h.url_for(action="view"))
            email(lca_info['proposal_update_email'], body)

        h.flash("Proposal %s edited!"%p_edit)
        return redirect_to('/proposal')

    @authorize(h.auth.has_reviewer_role)
    def review_index(self):
        c.person = h.signed_in_person()
        c.num_proposals = 0
        reviewer_role = Role.find_by_name('reviewer')
        c.num_reviewers = len(reviewer_role.people)
        for pt in c.proposal_types:
            stuff = Proposal.find_all_by_proposal_type_id(pt.id, include_withdrawn=False)
            c.num_proposals += len(stuff)
            setattr(c, '%s_collection' % pt.name, stuff)
        for aat in c.accommodation_assistance_types:
            stuff = Proposal.find_all_by_accommodation_assistance_type_id(aat.id)
            setattr(c, '%s_collection' % aat.name, stuff)
        for tat in c.travel_assistance_types:
            stuff = Proposal.find_all_by_travel_assistance_type_id(tat.id)
            setattr(c, '%s_collection' % tat.name, stuff)

        return render('proposal/list_review.mako')

    @authorize(h.auth.has_reviewer_role)
    def summary(self):
        c.proposal = {}
        for proposal_type in c.proposal_types:
            c.proposal[proposal_type] = Proposal.find_review_summary().filter(Proposal.type==proposal_type).filter(Proposal.status!=ProposalStatus.find_by_name('Withdrawn')).order_by('average').all()
        for aat in c.accommodation_assistance_types:
            stuff = Proposal.find_all_by_accommodation_assistance_type_id(aat.id)
            setattr(c, '%s_collection' % aat.name, stuff)
        for tat in c.travel_assistance_types:
            stuff = Proposal.find_all_by_travel_assistance_type_id(tat.id)
            setattr(c, '%s_collection' % tat.name, stuff)
        return render('proposal/summary.mako')

    def index(self):
        c.person = h.signed_in_person()
        return render('/proposal/list.mako')

    @dispatch_on(POST="_approve")
    @authorize(h.auth.has_organiser_role)
    def approve(self):
        c.highlight = set()
        c.proposals = Proposal.find_all()
        c.statuses = ProposalStatus.find_all()
        return render("proposal/approve.mako")

    @validate(schema=ApproveSchema(), form='approve', post_only=True, on_get=True, variable_decode=True)
    @authorize(h.auth.has_organiser_role)
    def _approve(self):
        c.highlight = set()
        talks = self.form_result['talk']
        statuses = self.form_result['status']
        for talk, status in zip(talks, statuses):
            if status is not None:
                c.highlight.add(talk.id)
                talk.status = status
        meta.Session.commit()

        c.proposals = Proposal.find_all()
        c.statuses = ProposalStatus.find_all()
        return render("proposal/approve.mako")

    @dispatch_on(POST="_withdraw")
    def withdraw(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)
        return render("/proposal/withdraw.mako")

    @validate(schema=ApproveSchema(), form='withdraw', post_only=True, on_get=True, variable_decode=True)
    def _withdraw(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.proposal = Proposal.find_by_id(id)
        status = ProposalStatus.find_by_name('Withdrawn')
        c.proposal.status = status
        meta.Session.commit()

        c.person = h.signed_in_person()

        # Make sure the organisers are notified of this
        c.email_address = h.lca_info['emails'][c.proposal.type.name.lower()]
        email(c.email_address, render('/proposal/withdraw_email.mako'))

        h.flash("Proposal withdrawn. The organisers have been notified.")
        return redirect_to(controller='proposal', action="index", id=None)

    @authorize(h.auth.has_organiser_role)
    def latex(self):
        c.proposal_type = ProposalType.find_all()

        for type in c.proposal_type:
          print type

        response.headers['Content-type']='text/plain; charset=utf-8'

        return render('/proposal/latex.mako')

    def clean_abstract(self, abstract):
        return abstract
        # why are we cleaning the abstract here? shouldn't the template engine take care of this?
        abs = h.html_clean(abstract)
        if abs.startswith("<p>") and abs.endswith("</p>"):
            return abs[3:-4]
        return abs
