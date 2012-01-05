import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

import datetime

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.ssl_requirement import enforce_ssl
from zookeepr.lib.validators import BaseSchema, ExistingRegistrationValidator, ExistingPersonValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model.vote import Vote, Person
from zookeepr.model.event import Event, EventValidator
from zookeepr.model.event_type import EventType
from zookeepr.model.schedule import Schedule
from zookeepr.model.time_slot import TimeSlot

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class VoteSchema(BaseSchema):
    rego_id = ExistingRegistrationValidator(not_empty=True)

class NewVoteSchema(BaseSchema):
    vote = VoteSchema()
    pre_validators = [NestedVariables]

class UpdateVoteSchema(BaseSchema):
    vote = VoteSchema()
    pre_validators = [NestedVariables]

class VoteController(BaseController):
    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        c.events = Event.find_all()
        c.schedule = Schedule.find_all()
        c.time_slot = TimeSlot.find_all()
        defaults = {
            'vote.vote_value': 1 
        }
        raw_params = request.params
        if 'rego_id' in raw_params:
            c.rego_id = int(raw_params['rego_id'])
            defaults['vote.rego_id'] = c.rego_id
        if 'event_id' in raw_params:
            c.event_id = int(raw_params['event_id'])
            defaults['vote.event_id'] = c.event_id

        form = render('/vote/new.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=NewVoteSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['vote']

        c.vote = Vote(**results)
        meta.Session.add(c.vote)
        meta.Session.commit()

        h.flash("Vote created")
        redirect_to(action='view', id=c.vote.id)

    def view(self, id):
        c.vote = Vote.find_by_id(id)
        return render('vote/view.mako')

    def index(self):
        c.vote_collection = Vote.find_all()
        return render('vote/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.vote = Vote.find_by_id(id)

        defaults = h.object_to_defaults(c.vote, 'vote')

        form = render('vote/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=UpdateVoteSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        vote = Vote.find_by_id(id)

        for key in self.form_result['vote']:
            setattr(vote, key, self.form_result['vote'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The note has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the rego note

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.vote = Vote.find_by_id(id)
        return render('vote/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.vote = Vote.find_by_id(id)
        meta.Session.delete(c.vote)
        meta.Session.commit()

        h.flash("Vote has been deleted.")
        redirect_to('index')
