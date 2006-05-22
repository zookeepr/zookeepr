from zookeepr.lib.base import *

class InfoController(BaseController):
    def index(self):
        h.redirect_to(action='whatson')

    def whatson(self):
        m.subexec('info/whatson.myt')

    def programme(self):
        m.subexec('info/programme.myt')

    def dates(self):
        m.subexec('info/dates.myt')

    def press(self):
        m.subexec('info/press.myt')

    def sydney(self):
        m.subexec('info/sydney.myt')

    def contact(self):
        m.subexec('info/contact.myt')

    def sponsors(self):
        m.subexec('info/sponsors.myt')
