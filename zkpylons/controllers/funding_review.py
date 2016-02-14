import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, FundingReviewSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import FundingReview

log = logging.getLogger(__name__)

class EditFundingReviewSchema(BaseSchema):
    review = FundingReviewSchema()
    pre_validators = [NestedVariables]

class FundingReviewController(BaseController):
    @authorize(h.auth.has_funding_reviewer_role)
    def __before__(self, **kwargs):
        return True

    def _is_reviewer(self):
        if not h.signed_in_person() is c.review.reviewer:
            h.auth.no_role()

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.form = 'edit'
        c.review = FundingReview.find_by_id(id)
        self._is_reviewer()

        c.funding = c.review.funding
        defaults = h.object_to_defaults(c.review, 'review')
        if defaults['review.score'] == None:
            defaults['review.score'] = 'null'
        if defaults['review.score'] == 1 or defaults['review.score'] == 2:
            defaults['review.score'] = '+%s'  % defaults['review.score']

        c.signed_in_person = h.signed_in_person()
        form = render('/funding_review/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditFundingReviewSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        c.review = FundingReview.find_by_id(id)
        self._is_reviewer()

        if self.form_result['review']['score'] == 'null':
            self.form_result['review']['score'] = None

        for key in self.form_result['review']:
            setattr(c.review, key, self.form_result['review'][key])

        # update the objects with the validated form data
        meta.Session.commit()

        h.flash("Review has been edited!")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        c.review = FundingReview.find_by_id(id)
        self._is_reviewer()
        
        return render('/funding_review/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.review = FundingReview.find_by_id(id)
        self._is_reviewer()

        meta.Session.delete(c.review)
        meta.Session.commit()

        h.flash("Review Deleted")
        redirect_to(controller='funding_review', action='index')

    def summary(self):
        c.review_collection=FundingReview.find_all()
        return render('funding_review/summary.mako')

    def index(self):
        c.review_collection = FundingReview.find_all()
        return render('funding_review/list.mako')

    def view(self, id):
        c.review = FundingReview.find_by_id(id)

        if c.review is None:
            redirect_to(action='index')

        return render('funding_review/view.mako')

