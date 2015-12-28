from .crud_helper import CrudHelper
from .fixtures import ScheduleFactory, TimeSlotFactory, LocationFactory, EventFactory, ConfigFactory

from routes import url_for
from .fixtures import PersonFactory, RoleFactory
from .utils import do_login

class TestSchedule(CrudHelper):
    def test_permissions(self, app, db_session):
        target = ScheduleFactory(event=EventFactory(title="empty causes errors"), time_slot=TimeSlotFactory(primary=True))
        ConfigFactory(key="time_zone", value="UTC") # Required for ical

        db_session.commit()

        # Public access: table, ical, json
        # View redirects to edit page
        CrudHelper.test_permissions(self, app, db_session, target=target, good_roles = ['public'], bad_roles = [], get_pages = ('table', 'ical', 'json'), post_pages=[])
        CrudHelper.test_permissions(self, app, db_session, target=target, dont_get_pages = 'view')

    def test_new(self, app, db_session):
        times = [TimeSlotFactory() for i in range(10)]
        locs  = [LocationFactory() for i in range(10)]
        events = [EventFactory(title="Must be set") for i in range(10)]
        db_session.commit()

        data = {
                "time_slot" : times[4].id,
                "location"  : locs[5].id,
                "event"     : events[6].id,
                "video_url" : "http://youtube.com/watch/me/love/me",
                "audio_url" : "http://hear.me/roar/",
                "slide_url" : "http://slippery.slope/",
                "overflow"  : False,
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        # Redirects to edit page
        target = ScheduleFactory()
        user = PersonFactory(roles = [RoleFactory(name = 'organiser')])
        db_session.commit()

        do_login(app, user)
        resp = app.get(url_for(controller='schedule', action='view', id=target.id))
        
        # Check for redirect
        assert resp.status_code == 302
        assert url_for(controller='schedule', action='edit', id=target.id) in resp.location

    def test_index(self, app, db_session):
        groups = [ScheduleFactory() for i in range(10)]
        db_session.commit()
        entries = { s.id : [str(s.id), s.time_slot.description, s.location.display_name] for s in groups }
        print entries

        CrudHelper.test_index(self, app, db_session, entries = entries, title="List Scheduled Events")

    def test_edit(self, app, db_session):
        times = [TimeSlotFactory() for i in range(10)]
        locs  = [LocationFactory() for i in range(10)]
        events = [EventFactory(title="Required") for i in range(10)]
        target = ScheduleFactory(time_slot=times[8], location=locs[7], event=events[6])
        db_session.commit()

        initial_values = {
                "time_slot" : str(target.time_slot.id),
                "location"  : str(target.location.id),
                "event"     : str(target.event.id),
                "video_url" : target.video_url,
                "audio_url" : target.audio_url,
                "slide_url" : target.slide_url,
                "overflow"  : target.overflow,
               }

        new_values = {
                "time_slot" : times[4].id,
                "location"  : locs[5].id,
                "event"     : events[6].id,
                "video_url" : "http://youtube.com/watch/me/love/me",
                "audio_url" : "http://hear.me/roar/",
                "slide_url" : "http://slippery.slope/",
                "overflow"  : False,
               }


        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target)

