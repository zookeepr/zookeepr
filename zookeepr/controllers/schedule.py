import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, abort
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

import formencode
from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from datetime import date, datetime, timedelta

from zookeepr.lib.mail import email
from zookeepr.lib.ordereddict import OrderedDict

from zookeepr.model import meta
from zookeepr.model.schedule import Schedule
from zookeepr.model.proposal import Proposal
from zookeepr.model.time_slot import TimeSlot, TimeSlotValidator
from zookeepr.model.location import Location, LocationValidator
from zookeepr.model.event import Event, EventValidator
from zookeepr.model.event_type import EventType

from zookeepr.config.lca_info import lca_info, file_paths

import os

log = logging.getLogger(__name__)

def get_directory_contents(directory):
    files = {}
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            if os.path.isfile(directory + "/" + filename):
                files[filename.rsplit('.')[0]] = filename
    return files

class NewScheduleFormSchema(BaseSchema):
    time_slot = TimeSlotValidator(if_missing=None)
    location = LocationValidator(if_missing=None)
    event = EventValidator(if_missing=None)

class ScheduleSchema(BaseSchema):
    time_slot = TimeSlotValidator(not_empty=True)
    location = LocationValidator(not_empty=True)
    event = EventValidator(not_empty=True)

class NewScheduleSchema(BaseSchema):
    schedule = ScheduleSchema()
    pre_validators = [NestedVariables]

class EditScheduleSchema(BaseSchema):
    schedule = ScheduleSchema()
    pre_validators = [NestedVariables]

class ScheduleController(BaseController):

    # Use this to limit to organisers only.
    #@authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        if h.signed_in_person():
            c.can_edit = h.signed_in_person().has_role('organiser')
        else:
            c.can_edit = False

        c.time_slots = TimeSlot.find_all()
        c.locations = Location.find_all()
        c.events = Event.find_all()

        c.get_talk = self._get_talk

        c.subsubmenu = []
#        query = """
#  SELECT DISTINCT date(scheduled) AS date
#  FROM proposal
#  WHERE scheduled IS NOT NULL
#  ORDER BY date;
#"""
#        res = meta.Session.execute(query)
#        for r in res.fetchall():
#           c.subsubmenu.append(( '/programme/schedule/' + r[0].lower(), r[1] ))
        c.subsubmenu.append([ '/programme/sunday', 'Sunday' ])
        c.scheduled_dates = TimeSlot.find_scheduled_dates()
        for scheduled_date in c.scheduled_dates:
            c.subsubmenu.append(['/programme/schedule/' + scheduled_date.strftime('%A').lower(), scheduled_date.strftime('%A')])

        c.subsubmenu.append([ '/programme/open_day', 'Saturday' ])

    def index(self, day=None):
        display_date = None

        available_days = {}
        for scheduled_date in c.scheduled_dates:
            available_days[scheduled_date.strftime('%A').lower()] = scheduled_date

        if day in available_days:
            display_date = available_days[day]

        if display_date is None:
            if date.today() in c.scheduled_dates:
                display_date = date.today()
            else:
                display_date = c.scheduled_dates[0]

        c.time_slots = TimeSlot.find_by_date(display_date)
        c.primary_times = {}
        for time_slot in TimeSlot.find_by_date(display_date, primary=True):
            c.primary_times[time_slot.start_time] = time_slot
        event_type = EventType.find_by_id(1)
        c.locations = Location.find_scheduled_by_date_and_type(display_date, event_type)

        c.time_increment = timedelta(minutes=5)
        c.time_increment_exclusive = timedelta(minutes=4, seconds=59, microseconds=999999)

        c.programme = OrderedDict()
        for time_slot in c.time_slots:
            time = time_slot.start_time
            while time < time_slot.end_time:
                schedules = Schedule.find_by_start_time(time, increment=c.time_increment_exclusive, exclusive=True)
                if schedules:
                    event = None
                    for schedule in schedules:
                        if event is None:
                            event = schedule.event
                        elif schedule.event != event:
                            raise "Bad"
                    c.programme[time] = {'exclusive': schedules}
                else:
                    schedules = []
                    for location in c.locations:
                        schedules.append(Schedule.find_by_start_time_and_location(time, location, increment=c.time_increment_exclusive))
                    for schedule in schedules:
                        if schedule is not None:
                            c.programme[time] = {'location': schedules}
                    if time not in c.programme:
                        c.programme[time] = None
                time = time + c.time_increment
        return render('/schedule/list.mako')

    @dispatch_on(POST="_new")
    @validate(schema=NewScheduleFormSchema(), on_get=True, post_only=False, variable_decode=True)
    def new(self):
        form = render('/schedule/new.mako')
        object = { 'schedule': self.form_result }
        defaults = NewScheduleSchema().from_python(object)
        return htmlfill.render(form, defaults)

    @validate(schema=NewScheduleSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['schedule']

        c.schedule = Schedule(**results)
        meta.Session.add(c.schedule)
        meta.Session.commit()

        h.flash("Schedule created")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.schedule = Schedule.find_by_id(id)
        defaults = {}
        defaults['schedule.time_slot'] = c.schedule.time_slot_id
        defaults['schedule.location'] = c.schedule.location_id
        defaults['schedule.event'] = c.schedule.event_id

        form = render('/schedule/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditScheduleSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        schedule = Schedule.find_by_id(id)

        for key in self.form_result['schedule']:
            setattr(schedule, key, self.form_result['schedule'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Schedule has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the schedule

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.schedule = Schedule.find_by_id(id)
        return render('/schedule/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.schedule = Schedule.find_by_id(id)
        meta.Session.delete(c.schedule)
        meta.Session.commit()

        h.flash("Schedule has been deleted.")
        redirect_to('index')

# Old Controller Starts here
    day_dates = {'monday':    date(2011,1,24),
                 'tuesday':   date(2011,1,25),
                 'wednesday': date(2011,1,26),
                 'thursday':  date(2011,1,27),
                 'friday':    date(2011,1,28),
                 'saturday':  date(2011,1,29)}

    def _get_talk(self, talk_id):
        """ Return a proposal object """
        return Proposal.find_by_id(id=talk_id, abort_404=False)

    def view_miniconf(self, id):
        try:
            c.day = request.GET['day']
        except:
            c.day = 'all'
        try:
            c.talk = Proposal.find_accepted_by_id(id)
        except:
            c.talk_id = id
            c.webmaster_email = lca_info['webmaster_email']
            return render('/schedule/invalid_talkid.mako')

        return render('/schedule/view_miniconf.mako')

    def view_talk(self, id):
        try:
            c.day = request.GET['day']
        except:
            c.day = 'all'
        try:
            c.talk = Proposal.find_accepted_by_id(id)
        except:
            c.talk_id = id
            c.webmaster_email = lca_info['webmaster_email']
            return render('/schedule/invalid_talkid.mako')

        return render('/schedule/view_talk.mako')

    def old_index(self):
        # get list of slides as dict
        c.slide_list = {}
        if file_paths.has_key('slides_path') and file_paths['slides_path'] != '':
            c.slide_list = get_directory_contents(file_paths['slides_path'])
            c.download_path = file_paths['slides_html']

        c.ogg_list = {} # TODO: fill these in
        if file_paths.has_key('ogg_path') and file_paths['ogg_path'] != '':
            c.ogg_path = file_paths['ogg_path']

        c.speex_list = {} # TODO: fill these in
        if file_paths.has_key('speex_path') and file_paths['speex_path'] != '':
            c.speex_path =  file_paths['speex_path']

        c.talks = Proposal.find_all_accepted()
        if c.day in self.day_dates:
            # this won't work across months as we add a day to get a 24 hour range period and that day can overflow from Jan. (we're fine for 09!)
            c.talks = c.talks.filter(Proposal.scheduled >= self.day_dates[c.day] and Proposal.scheduled < self.day_dates[c.day].replace(day=self.day_dates[c.day].day+1))
        c.programme = OrderedDict()
        c.talks.order_by(Proposal.scheduled.asc(), Proposal.finished.desc()).all()
        for talk in c.talks:
            if isinstance(talk.scheduled, date):
                talk_day = talk.scheduled.strftime('%A')
                if c.programme.has_key(talk_day) is not True:
                    c.programme[talk_day] = OrderedDict()
                if talk.building is not None:
                    if c.programme[talk_day].has_key(talk.building) is not True:
                        c.programme[talk_day][talk.building] = OrderedDict()
                    if c.programme[talk_day][talk.building].has_key(talk.theatre) is not True:
                        c.programme[talk_day][talk.building][talk.theatre] = []
                    c.programme[talk_day][talk.building][talk.theatre].append(talk)
        if day is not None and os.path.isfile('zookeepr/templates/schedule/' + day + '.mako'):
            c.day = day
            return render('/schedule/list.mako')

        return render('/schedule/list.mako')

    _ROOMS = (
        ('mfc', 'Auditorium', None),
        ('_mfc_384', 'Auditorium', 'r2-stream-1'),
        ('_mfc_128', 'Auditorium', 'r2-stream-2'),
        ('_mfc_56', 'Auditorium', 'r2-stream-3'),
        ('_mfc_28a', 'Auditorium', 'r2-stream-4'),
        #('_mfc_mfc-slides', 'Auditorium', ''),
        ('illott', 'Ilott Theatre', 'r2-stream-16'),
        ('renouf-1', 'Renouf 1', 'r2-stream-11'),
        ('renouf-2', 'Renouf 2', 'r2-stream-12'),
        ('civic-1', 'Civic Suites 1 & 2', 'r2-stream-14'),
        ('ftaplin', 'Frank Taplin', 'r2-stream-13'),
        ('civic-3', 'Civic Suite 3', 'r2-stream-15'),
    )
    _ROOMS_D = dict([(r[0], (r[1], r[2])) for r in _ROOMS])

    def video_room(self, room=None):
        c.all_rooms = self._ROOMS

        if room in self._ROOMS_D:
            c.room_id = room
            c.room_name = self._ROOMS_D[room][0]
            c.room_stream_id = self._ROOMS_D[room][1]
            if room.startswith('_'):
                c.room_id = c.room_id.split('_')[2]
        else:
            c.room_id = None
            c.room_name = None
            c.room_stream_id = None

        return render('/schedule/video_room.mako')
