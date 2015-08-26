import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.event_type import EventType

log = logging.getLogger(__name__)

class EventTypeSchema(BaseSchema):
    name = validators.String(not_empty=True)

class NewEventTypeSchema(BaseSchema):
    event_type = EventTypeSchema()
    pre_validators = [NestedVariables]

class EditEventTypeSchema(BaseSchema):
    event_type = EventTypeSchema()
    pre_validators = [NestedVariables]

class EventTypeController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new")
    def new(self):
        return render('/event_type/new.mako')

    @validate(schema=NewEventTypeSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['event_type']

        c.event_type = EventType(**results)
        meta.Session.add(c.event_type)
        meta.Session.commit()

        h.flash("Event Type created")
        redirect_to(action='index')

    def index(self):
        c.can_edit = True
        c.event_type_collection = EventType.find_all()
        return render('/event_type/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.event_type = EventType.find_by_id(id)

        defaults = h.object_to_defaults(c.event_type, 'event_type')

        form = render('/event_type/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditEventTypeSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        event_type = EventType.find_by_id(id)

        for key in self.form_result['event_type']:
            setattr(event_type, key, self.form_result['event_type'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Event Type has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the event_type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.event_type = EventType.find_by_id(id)
        return render('/event_type/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.event_type = EventType.find_by_id(id)
        meta.Session.delete(c.event_type)
        meta.Session.commit()

        h.flash("Event Type has been deleted.")
        redirect_to('index')
