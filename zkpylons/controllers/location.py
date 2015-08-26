import logging
import vobject

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
from zkpylons.model.location import Location
from zkpylons.model.config import Config

log = logging.getLogger(__name__)

class LocationSchema(BaseSchema):
    display_name = validators.String(not_empty=True)
    display_order = validators.Int()
    capacity = validators.Int()

class NewLocationSchema(BaseSchema):
    location = LocationSchema()
    pre_validators = [NestedVariables]

class EditLocationSchema(BaseSchema):
    location = LocationSchema()
    pre_validators = [NestedVariables]

class LocationController(BaseController):

    @enforce_ssl(required_all=True)
    def __before__(self, **kwargs):
        c.can_edit = True

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_new")
    def new(self):
        return render('/location/new.mako')

    @authorize(h.auth.has_organiser_role)
    @validate(schema=NewLocationSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['location']

        c.location = Location(**results)
        meta.Session.add(c.location)
        meta.Session.commit()

        h.flash("Location created")
        redirect_to(action='index', id=None)

    @authorize(h.auth.has_organiser_role)
    def view(self, id):
        c.location = Location.find_by_id(id)
        return render('/location/view.mako')

    @authorize(h.auth.has_organiser_role)
    def index(self):
        c.location_collection = Location.find_all()
        return render('/location/list.mako')

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.location = Location.find_by_id(id)

        defaults = h.object_to_defaults(c.location, 'location')

        form = render('/location/edit.mako')
        return htmlfill.render(form, defaults)

    @authorize(h.auth.has_organiser_role)
    @validate(schema=EditLocationSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        location = Location.find_by_id(id)

        for key in self.form_result['location']:
            setattr(location, key, self.form_result['location'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Location has been updated successfully.")
        redirect_to(action='index', id=None)

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the location

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.location = Location.find_by_id(id)
        return render('/location/confirm_delete.mako')

    @authorize(h.auth.has_organiser_role)
    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.location = Location.find_by_id(id)
        meta.Session.delete(c.location)
        meta.Session.commit()

        h.flash("Location has been deleted.")
        redirect_to('index')

    def ical(self, id):
        c.schedule_collection = Location.find_by_id(id).schedule

        ical = vobject.iCalendar()
        for schedule in c.schedule_collection:
            if not schedule.time_slot.heading:
                event = ical.add('vevent')
                event.add('uid').value = str(schedule.id) + '@' + Config.get('event_host')
                # Created
                tz = timezone(Config.get('time_zone'))
                event.add('created').value = schedule.creation_timestamp.replace(tzinfo=tz)
                # Last Modified
                event.add('dtstamp').value = schedule.last_modification_timestamp.replace(tzinfo=tz)
                event.add('last-modified').value = schedule.last_modification_timestamp.replace(tzinfo=tz)
                # Start and End Time
                event.add('dtstart').value = schedule.time_slot.start_time.replace(tzinfo=tz)
                event.add('dtend').value = schedule.time_slot.end_time.replace(tzinfo=tz)
                # Title and Author (need to add Author here)
                event.add('summary').value = schedule.event.computed_title() + '. ' + h.list_to_string(schedule.event.computed_speakers())
                # Abstract, if we have one
                event.add('description').value = schedule.event.computed_abstract()
                # Add a URL
                if schedule.event.proposal:
                    event.add('url').value = h.url_for(qualified=True, controller='schedule', action='view_talk', id=schedule.event.proposal.id)
                elif not (schedule.event.url is None or schedule.event.url == ''):
                    if schedule.event.url.startswith('https://') or schedule.event.url.startswith('http://'):
                        event.add('url').value = h.url_for(str(schedule.event.url))
                    else:
                        event.add('url').value = h.url_for(str(schedule.event.url), qualified=True)

                concurrent_schedules = schedule.event.schedule_by_time_slot(schedule.time_slot)
                for concurrent_schedule in concurrent_schedules:
                    if concurrent_schedule != schedule:
                        if concurrent_schedule in c.schedule_collection:
                            c.schedule_collection.remove(concurrent_schedule)

                locations = [concurrent_schedule.location.display_name for concurrent_schedule in concurrent_schedules]
                event.add('location').value = h.list_to_string(locations)

        response.charset = 'utf8'
        response.headers['content-type'] = 'text/calendar; charset=utf8'
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')
        return ical.serialize()

