import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, abort
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from datetime import date, datetime

from zookeepr.lib.mail import email
from zookeepr.lib.sort import odict

from zookeepr.model import meta, Proposal

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


class ScheduleController(BaseController):
    day_dates = {'monday':    date(2010,1,18),
                 'tuesday':   date(2010,1,19),
                 'wednesday': date(2010,1,20),
                 'thursday':  date(2010,1,21),
                 'friday':    date(2010,1,22),
                 'saturday':  date(2010,1,23)}

    # Use this to limit to organisers only.
    #@authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
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
        c.subsubmenu = [
          [ '/programme/sunday',             'Sunday' ],
          [ '/programme/schedule/monday',    'Monday' ],
          [ '/programme/schedule/tuesday',   'Tuesday' ],
          [ '/programme/schedule/wednesday', 'Wednesday' ],
          [ '/programme/schedule/thursday',  'Thursday' ],
          [ '/programme/schedule/friday',    'Friday' ],
          [ '/programme/open_day',           'Saturday' ],
        ]

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

    def index(self, day=None):
        if day == None:
            for weekday in self.day_dates:
                if self.day_dates[weekday] == datetime.today().date():
                    c.day = weekday
            if c.day == None:
                c.day = 'monday'
        else:
            c.day = day.lower()

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
        c.programme = odict()
        c.talks.order_by(Proposal.scheduled.asc(), Proposal.finished.desc()).all()
        for talk in c.talks:
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
        return render('/schedule/list.mako')
