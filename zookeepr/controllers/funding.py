import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, DictSet, PersonValidator
from zookeepr.lib.validators import ExistingPersonValidator
from zookeepr.lib.validators import FundingValidator, FileUploadValidator
from zookeepr.lib.validators import PersonSchema, FundingTypeValidator
from zookeepr.lib.validators import FundingStatusValidator, PrevLCAValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Funding, FundingType, FundingStatus, FundingAttachment, Person

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class FundingSchema(BaseSchema):
    allow_extra_fields = False

    male = validators.Int(min=0, max=1)
    why_attend = validators.String(not_empty=True)
    how_contribute = validators.String(not_empty=True)
    financial_circumstances = validators.String(not_empty=True)
    type = FundingTypeValidator()
    diverse_groups = validators.String()
    supporting_information = validators.String()
    prevlca = DictSet(if_missing=None)

    chained_validators = [PrevLCAValidator()]

class NewFundingSchema(BaseSchema):
    funding = FundingSchema()
    attachment1 = FileUploadValidator()
    attachment2 = FileUploadValidator()
    pre_validators = [NestedVariables]

class ExistingFundingSchema(BaseSchema):
    funding = FundingSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

class NewAttachmentSchema(BaseSchema):
    attachment = FileUploadValidator(not_empty=True)
    pre_validators = [NestedVariables]

class ApproveSchema(BaseSchema):
    funding = ForEach(FundingValidator())
    status = ForEach(FundingStatusValidator())

class FundingController(BaseController):

    def __init__(self, *args):
        c.funding_status = lca_info['funding_status']
        c.funding_editing = lca_info['funding_editing']

    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        c.funding_types = FundingType.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        if c.funding_status == 'closed':
           if not h.auth.authorized(h.auth.has_late_submitter_role):
              return render("funding/closed.mako")
        elif c.funding_status == 'not_open':
           return render("funding/not_open.mako")

        c.person = h.signed_in_person()

        defaults = {
            'funding.type': 1,
        }
        form = render("funding/new.mako")
        return htmlfill.render(form, defaults)

    @validate(schema=NewFundingSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        if c.funding_status == 'closed':
            return render("funding/closed.mako")
        elif c.funding_status == 'not_open':
           return render("funding/not_open.mako")

        funding_results = self.form_result['funding']
        attachment_results1 = self.form_result['attachment1']
        attachment_results2 = self.form_result['attachment2']

        c.person = h.signed_in_person()

        c.funding = Funding(**funding_results)
        c.funding.status = FundingStatus.find_by_name('Pending')
        c.funding.person = c.person

        if not c.funding.type.available():
            return render("funding/type_unavailable.mako")

        meta.Session.add(c.funding)

        if attachment_results1 is not None:
            attachment = FundingAttachment(**attachment_results1)
            c.funding.attachments.append(attachment)
            meta.Session.add(attachment)
        if attachment_results2 is not None:
            attachment = FundingAttachment(**attachment_results2)
            c.funding.attachments.append(attachment)
            meta.Session.add(attachment)

        meta.Session.commit()
        email(c.funding.person.email_address, render('funding/thankyou_email.mako'))

        h.flash("Funding submitted!")
        return redirect_to(controller='funding', action="index", id=None)

    @dispatch_on(POST="_attach")
    def attach(self, id):
        return render('funding/attach.mako')


    @validate(schema=NewAttachmentSchema(), form='attach', post_only=True, on_get=True, variable_decode=True)
    def _attach(self, id):
        """Attach a file to the funding.
        """
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.funding = Funding.find_by_id(id)

        attachment_results = self.form_result['attachment']
        attachment = FundingAttachment(**attachment_results)

        c.funding.attachments.append(attachment)

        meta.Session.commit()

        h.flash("File was attached")

        return redirect_to(action='view', id=id)

    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(id), h.auth.has_organiser_role, h.auth.has_reviewer_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.funding = Funding.find_by_id(id)

        return render('funding/view.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        if not h.auth.authorized(h.auth.has_organiser_role):
            if c.funding_editing == 'closed':
                return render("funding/editing_closed.mako")
            elif c.funding_editing == 'not_open':
                return render("funding/editing_not_open.mako")

        c.funding = Funding.find_by_id(id)

        defaults = {}
        defaults.update(h.object_to_defaults(c.funding, 'funding'))
        # This is horrible, don't know a better way to do it
        if c.funding.type:
            defaults['funding.type'] = defaults['funding.funding_type_id']
        if c.funding.male:
            defaults['funding.male'] = 1
        else:
            defaults['funding.male'] = 0

        form = render('/funding/edit.mako')
        return htmlfill.render(form, defaults)


    @validate(schema=ExistingFundingSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        if not h.auth.authorized(h.auth.has_organiser_role):
            if c.funding_editing == 'closed':
                return render("funding/editing_closed.mako")
            elif c.funding_editing == 'not_open':
                return render("funding/editing_not_open.mako")

        c.funding = Funding.find_by_id(id)
        for key in self.form_result['funding']:
            setattr(c.funding, key, self.form_result['funding'][key])

        c.person = self.form_result['person_to_edit']

        meta.Session.commit()

        h.flash("Funding for %s edited!"%c.person.first_name)
        return redirect_to('/funding')

    def index(self):
        c.person = h.signed_in_person()
        return render('/funding/list.mako')

    @dispatch_on(POST="_approve")
    @authorize(h.auth.Or(h.auth.has_funding_reviewer_role, h.auth.has_organiser_role))
    def approve(self):
        c.highlight = set()
        c.funding_requests = Funding.find_all()
        c.statuses = FundingStatus.find_all()
        return render("funding/approve.mako")

    @validate(schema=ApproveSchema(), form='approve', post_only=True, on_get=True, variable_decode=True)
    @authorize(h.auth.Or(h.auth.has_funding_reviewer_role, h.auth.has_organiser_role))
    def _approve(self):
        c.highlight = set()
        requests = self.form_result['request']
        statuses = self.form_result['status']
        for request, status in zip(requests, statuses):
            if status is not None:
                c.highlight.add(request.id)
                request.status = status
        meta.Session.commit()

        c.funding = Funding.find_all()
        c.statuses = FundingStatus.find_all()
        return render("funding/approve.mako")

    @dispatch_on(POST="_withdraw")
    def withdraw(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.funding = Funding.find_by_id(id)
        return render("/funding/withdraw.mako")

    @validate(schema=ApproveSchema(), form='withdraw', post_only=True, on_get=True, variable_decode=True)
    def _withdraw(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_funding_submitter(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.funding = Funding.find_by_id(id)
        status = FundingStatus.find_by_name('Withdrawn')
        c.funding.status = status
        meta.Session.commit()

        c.person = h.signed_in_person()

        # Make sure the organisers are notified of this
        c.email_address = h.lca_info['emails']['funding']
        email(c.email_address, render('/funding/withdraw_email.mako'))

        h.flash("Funding withdrawn. The organisers have been notified.")
        return redirect_to(controller='funding', action="index", id=None)
