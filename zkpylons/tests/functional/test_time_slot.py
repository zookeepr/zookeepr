from routes import url_for
from BeautifulSoup import BeautifulSoup

from .crud_helper import CrudHelper
from .fixtures import TimeSlotFactory, ScheduleFactory

class TestTimeSlot(CrudHelper):
    def test_new(self, app, db_session):
        data = {
                "primary"    : False,
                "heading"    : True,
               }

        def extra_form_check(form):
            assert 'time_slot.start_date' in form.fields
            assert 'time_slot.start_time' in form.fields
            assert 'time_slot.end_date' in form.fields
            assert 'time_slot.end_time' in form.fields

        def extra_form_set(form):
            form['time_slot.start_date'] = "28/07/1914"
            form['time_slot.start_time'] = "05:00"
            form['time_slot.end_date'] = "11/11/1917"
            form['time_slot.end_time'] = "15:30"

        def extra_data_check(new):
            assert new.start_time.isoformat() == "1914-07-28T05:00:00"
            assert new.end_time.isoformat() == "1917-11-11T15:30:00"

        CrudHelper.test_new(self, app, db_session, data=data, extra_form_check = extra_form_check, extra_form_set=extra_form_set, extra_data_check = extra_data_check)

    def test_view(self, app, db_session):
        schedules = [ScheduleFactory() for i in range(10)]
        target = TimeSlotFactory(schedule=schedules)

        db_session.commit()
        expected = [target.start_time.strftime('%d/%m/%y %H:%M:%S'), target.end_time.strftime('%d/%m/%y %H:%M:%S'), str(target.id)]
        resp = CrudHelper.test_view(self, app, db_session, target=target, expected=expected)

        # View also lists scheduled events in this time slot
        soup = BeautifulSoup(resp.body)
        schedule_table = soup.find('table')
        rows = schedule_table.findAll('tr')

        # 1 row per schedule, 1 heading, 1 footer
        assert len(rows) == len(schedules) + 1 + 1

        del rows[0] # Throw away header

        # Last row should contain a link to add to the schedule
        footer = rows.pop()
        assert url_for(controller='schedule', action='new', id=None) in str(footer)

        for i in range(len(rows)):
            # Each row is ordered by id, same as props
            # Each row should contain a link to the location view page and display_name
            # Each row should contain a link to the event view page and computed_title()
            # Each row should contain a link to the schedule edit and delete pages
            row_str = str(rows[i])
            sched = schedules[i]
            assert url_for(controller='location', action='view', id=sched.location.id) in row_str
            assert sched.location.display_name in row_str
            assert url_for(controller='event', action='view', id=sched.event.id) in row_str
            if sched.event.computed_title() is not None:
                assert sched.event.computed_title() in row_str
            assert url_for(controller='schedule', action='edit', id=sched.id) in row_str
            assert url_for(controller='schedule', action='delete', id=sched.id) in row_str

    def test_index(self, app, db_session):
        groups = [TimeSlotFactory() for i in range(10)]
        db_session.commit()
        entries = { s.id : [str(s.id), s.start_time.strftime('%d/%m/%y %H:%M:%S'), s.end_time.strftime('%d/%m/%y %H:%M:%S')] for s in groups }

        CrudHelper.test_index(self, app, db_session, entries = entries)

    def test_edit(self, app, db_session):
        target = TimeSlotFactory(start_time="1939-09-01T1800", end_time="1945-09-02T1215")
        db_session.commit()

        initial_values = {
                "start_date" : "01/09/1939",
                "start_time" : "18:00",
                "end_date"   : "02/09/1945",
                "end_time"   : "12:15",
                "primary"    : target.primary,
                "heading"    : target.heading,
               }

        new_values = {
                "primary"    : False,
                "heading"    : True,
               }

        def extra_form_set(form):
            form['time_slot.start_date'] = "28/07/1914"
            form['time_slot.start_time'] = "05:00"
            form['time_slot.end_date'] = "11/11/1917"
            form['time_slot.end_time'] = "15:30"

        def extra_data_check(new):
            assert new.start_time.isoformat() == "1914-07-28T05:00:00"
            assert new.end_time.isoformat() == "1917-11-11T15:30:00"


        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target, extra_form_set=extra_form_set, extra_data_check = extra_data_check)
