import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

import datetime

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ExistingRegistrationValidator, ExistingPersonValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.vote import Vote, Person
from zkpylons.model.event import Event, EventValidator
from zkpylons.model.event_type import EventType
from zkpylons.model.schedule import Schedule
from zkpylons.model.time_slot import TimeSlot

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
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        c.signed_in_person = h.signed_in_person()
        c.events = Event.find_all()
        c.schedule = Schedule.find_all()
        c.time_slot = TimeSlot.find_all()
        if not c.signed_in_person.registration:
          return render('/vote/no_rego.mako')
        c.votes = Vote.find_by_rego(c.signed_in_person.registration.id)
        defaults = {
            'vote.vote_value': 1 
        }
        args = request.GET
        eventid = args.get('eventid',0)
        revoke = args.get('revoke',0)
        c.eventid = eventid
        if int(eventid) != 0 and c.votes.count() < 4 and revoke == 0:
            c.vote = Vote()
            c.vote.rego_id = c.signed_in_person.registration.id
            c.vote.vote_value = 1
            c.vote.event_id = eventid
            meta.Session.add(c.vote)
            meta.Session.commit()
        if int(eventid) != 0 and int(revoke) != 0:
            c.vote = Vote.find_by_event_rego(eventid,c.signed_in_person.registration.id)
            meta.Session.delete(c.vote)
            meta.Session.commit()
            redirect_to('new')
  

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

#    def view(self, id):
 #       args = request.GET
 #       eventid = int(args.get('eventid',0))
 #       c.signed_in_person = h.signed_in_person()
 #       c.vote = Vote.find_by_event_rego(eventid,c.signed_in_person.registration.id)
 #       return render('vote/view.mako')

    def index(self):
        c.vote_collection = Vote.find_all()
        # return render('vote/list.mako')
        redirect_to(action='new')

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

    @dispatch_on(POST="_revoke") 
    def revoke(self):
        """Delete the rego note

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        args = request.GET
        eventid = int(args.get('eventid',0))
        c.signed_in_person = h.signed_in_person()
        c.vote = Vote.find_by_event_rego(eventid,c.signed_in_person.registration.id)
        meta.Session.delete(c.vote)
        meta.Session.commit()
        form = render('/vote/delete.mako')
        return htmlfill.render(form, defaults)
        redirect_to('new')

    @validate(schema=None, form='revoke', post_only=True, on_get=True, variable_decode=True)
    def _revoke(self):
        args = request.GET
        eventid = int(args.get('eventid',0))
        c.signed_in_person = h.signed_in_person()
        c.vote = Vote.find_by_event_rego(eventid,c.signed_in_person.registration.id)
        meta.Session.delete(c.vote)
        meta.Session.commit()
        redirect_to('new')


