import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, ReviewSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Review, Stream

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class EditReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [NestedVariables]

class ReviewController(BaseController):
    @authorize(h.auth.has_reviewer_role)
    def __before__(self, **kwargs):
        c.streams = Stream.find_all()

    def _is_reviewer(self):
        if not h.signed_in_person() is c.review.reviewer:
            h.auth.no_role()

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.form = 'edit'
        c.review = Review.find_by_id(id)
        self._is_reviewer()

        c.proposal = c.review.proposal
        defaults = h.object_to_defaults(c.review, 'review')

        c.signed_in_person = h.signed_in_person()
        form = render('/review/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditReviewSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        c.review = Review.find_by_id(id)
        self._is_reviewer()

        for key in self.form_result['review']:
            setattr(c.review, key, self.form_result['review'][key])

        # update the objects with the validated form data
        meta.Session.commit()

        h.flash("Review has been edited!")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        c.review = Review.find_by_id(id)
        
        if c.review.reviewer.id != h.signed_in_person().id:
            # Raise a no_auth error
            h.auth.no_role()

        return render('/review/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.review = Review.find_by_id(id)

        if c.review.reviewer.id != h.signed_in_person().id:
            # Raise a no_auth error
            h.auth.no_role()

        meta.Session.delete(c.review)
        meta.Session.commit()

        h.flash("Review Deleted")
        redirect_to(controller='review', action='index')

    def summary(self):
        c.review_collection=Review.find_all()
        return render('review/summary.mako')

    def index(self):
        c.review_collection = Review.find_all()
        return render('/review/list.mako')

    def view(self, id):
        c.review = Review.find_by_id(id)

        # TODO: currently not enough (see TODOs in model/proposal.py)
        #if not h.auth.authorized(h.auth.has_organiser_role):
        #    # You can't review your own proposal
        #    for person in c.review.proposal.people:
        #        if person.id == h.signed_in_person().id:
        #            h.auth.no_role()

        if c.review is None:
            redirect_to(action='index')

        return render('review/view.mako')

