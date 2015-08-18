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
from zkpylons.model.config import Config

from zkpylons.controllers.proposal import NewProposalSchema

from zkpylons.lib.validators import ReviewSchema

log = logging.getLogger(__name__)

class MiniconfProposalController(BaseController):

    def __init__(self, *args):
        c.cfp_status       = Config.get('cfp_status')
        c.cfmini_status    = Config.get('cfmini_status')
        c.proposal_editing = Config.get('proposal_editing')

    @authorize(h.auth.is_valid_user)
    @authorize(h.auth.is_activated_user)
    def __before__(self, **kwargs):
        c.proposal_types = ProposalType.find_all()
        c.target_audiences = TargetAudience.find_all()
        c.accommodation_assistance_types = AccommodationAssistanceType.find_all()
        c.travel_assistance_types = TravelAssistanceType.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        # call for miniconfs has closed
        if c.cfmini_status == 'closed':
            return render("proposal/closed_mini.mako")
        elif c.cfmini_status == 'not_open':
            return render("proposal/not_open_mini.mako")

        c.proposal_type = ProposalType.find_by_name('Miniconf')
        c.person = h.signed_in_person()
        h.check_for_incomplete_profile(c.person)

        defaults = {
            'proposal.type': c.proposal_type.id,
            'proposal.technical_requirements': "",
            'proposal.accommodation_assistance': 1,
            'proposal.travel_assistance': 1,
            'proposal.video_release': 0,
            'proposal.slides_release': 0,
            'person.name' : c.person.fullname,
            'person.mobile' : c.person.mobile,
            'person.experience' : c.person.experience,
            'person.bio' : c.person.bio,
        }
 
        form = render("proposal/new_mini.mako")
        return htmlfill.render(form, defaults)

    @validate(schema=NewProposalSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        person_results = self.form_result['person']
        proposal_results = self.form_result['proposal']
        attachment_results = self.form_result['attachment']

        proposal_results['status'] = ProposalStatus.find_by_name('Pending Review')

        c.proposal = Proposal(**proposal_results)
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
        email(c.person.email_address, render('proposal/thankyou_mini_email.mako'))

        h.flash("Proposal submitted!")
        return redirect_to(controller='proposal', action="index", id=None)

    def index(self):
        return redirect_to(controller='proposal', action="index", id=None)

