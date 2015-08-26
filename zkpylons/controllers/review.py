import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, ReviewSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Review, Stream, Person, ProposalType, Proposal

log = logging.getLogger(__name__)

class ReviewController(BaseController):
    @authorize(h.auth.has_reviewer_role)
    def __before__(self, **kwargs):
        c.streams = Stream.select_values()

    def _is_reviewer(self):
        if not h.signed_in_person() is c.review.reviewer:
            h.auth.no_role()

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.review = Review.find_by_id(id)

        redirect_to(h.url_for(controller='proposal', id=c.review.proposal.id, action='review'))

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
        c.summary = Person.find_review_summary().all()
        return render('review/summary.mako')

    def index(self):
        c.proposal_type_collection = ProposalType.find_all()

        c.review_collection_by_type = {}
        for proposal_type in c.proposal_type_collection:
            query = Review.by_reviewer(h.signed_in_person()).join(Proposal).filter_by(proposal_type_id=proposal_type.id)
            c.review_collection_by_type[proposal_type] = query.all()
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

