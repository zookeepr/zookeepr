from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View
from zookeepr import model
from zookeepr.model import Proposal
from zookeepr.lib.base import *

from datetime import date, datetime
from zookeepr.lib.sort import odict


class ScheduleController(BaseController):
    day_dates = {'monday':    date(2009,1,19),
                 'tuesday':   date(2009,1,20),
                 'wednesday': date(2009,1,21),
                 'thursday':  date(2009,1,22),
                 'friday':    date(2009,1,23),
                 'saturday':  date(2009,1,24)}

    def index(self, day):
        talks = self.dbsession.query(Proposal).filter_by(accepted=True)
        if day.lower() in self.day_dates:
            # this won't work across months as we add a day to get a 24 hour range period and that day can overflow from Jan. (we're fine for 09!)
            talks = talks.filter(Proposal.scheduled >= self.day_dates[day.lower()] and Proposal.scheduled < self.day_dates[day.lower()].replace(day=self.day_dates[day.lower()].day+1))
        c.programme = odict()
        for talk in talks.order_by((Proposal.scheduled.asc(), Proposal.finished.desc())).all():
            if isinstance(talk.scheduled, date):
                talk_day = talk.scheduled.strftime('%A')
                if c.programme.has_key(talk_day) is not True:
                    c.programme[talk_day] = odict()
                if talk.building is not None:
                    if c.programme[talk_day].has_key(talk.building) is not True:
                        c.programme[talk_day][talk.building] = odict()
                    if c.programme[talk_day][talk.building].has_key(talk.theatre) is not True:
                        c.programme[talk_day][talk.building][talk.theatre] = []
                    c.programme[talk_day][talk.building][talk.theatre].append(talk)
        return render_response('schedule/table.myt')
