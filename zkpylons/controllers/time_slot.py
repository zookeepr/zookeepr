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
from zkpylons.model.time_slot import TimeSlot

from datetime import datetime

log = logging.getLogger(__name__)

class TimeSlotSchema(BaseSchema):
    start_date = validators.DateConverter(month_style='dd/mm/yyyy')
    start_time = validators.TimeConverter(use_datetime=True)
    end_date = validators.DateConverter(month_style='dd/mm/yyyy')
    end_time = validators.TimeConverter(use_datetime=True)
    primary = validators.Bool()
    heading = validators.Bool()

class NewTimeSlotSchema(BaseSchema):
    time_slot = TimeSlotSchema()
    pre_validators = [NestedVariables]

class EditTimeSlotSchema(BaseSchema):
    time_slot = TimeSlotSchema()
    pre_validators = [NestedVariables]

class TimeSlotController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/time_slot/new.mako')

    @validate(schema=NewTimeSlotSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['time_slot']
        results['start_time'] = datetime.combine(results['start_date'], results['start_time'])
        results['end_time'] = datetime.combine(results['end_date'], results['end_time'])
        del results['start_date']
        del results['end_date']

        c.time_slot = TimeSlot(**results)
        meta.Session.add(c.time_slot)
        meta.Session.commit()

        h.flash("Time Slot created")
        redirect_to(action='index')

    def view(self, id):
        c.time_slot = TimeSlot.find_by_id(id)
        return render('/time_slot/view.mako')

    def index(self):
        c.time_slot_collection = TimeSlot.find_all()
        return render('/time_slot/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.time_slot = TimeSlot.find_by_id(id)

        defaults = h.object_to_defaults(c.time_slot, 'time_slot')
        defaults['time_slot.start_date'] = c.time_slot.start_time.strftime('%d/%m/%Y')
        defaults['time_slot.start_time'] = c.time_slot.start_time.strftime('%H:%M')
        defaults['time_slot.end_date'] = c.time_slot.end_time.strftime('%d/%m/%Y')
        defaults['time_slot.end_time'] = c.time_slot.end_time.strftime('%H:%M')

        form = render('/time_slot/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditTimeSlotSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        time_slot = TimeSlot.find_by_id(id)

        for key in self.form_result['time_slot']:
            setattr(time_slot, key, self.form_result['time_slot'][key])

        results = self.form_result['time_slot']
        time_slot.start_time=datetime.combine(results['start_date'], results['start_time'])
        time_slot.end_time=datetime.combine(results['end_date'], results['end_time'])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Time Slot has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the time_slot

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.time_slot = TimeSlot.find_by_id(id)
        return render('/time_slot/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.time_slot = TimeSlot.find_by_id(id)
        meta.Session.delete(c.time_slot)
        meta.Session.commit()

        h.flash("Time Slot has been deleted.")
        redirect_to('index')
