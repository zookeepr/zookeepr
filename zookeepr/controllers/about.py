from zookeepr.lib.base import *

class InfoController(BaseController):
    def index(self):
        h.redirect_to(action='whatson')

    def whatson(self):
        m.subexec('about/whatson.myt')

    def programme(self):
        m.subexec('about/programme.myt')

    def dates(self):
        m.subexec('about/dates.myt')

    def press(self):
        m.subexec('about/press.myt')

    def sydney(self):
        m.subexec('about/sydney.myt')

    def contact(self):
        m.subexec('about/contact.myt')

    def sponsors(self):
        m.subexec('about/sponsors.myt')
