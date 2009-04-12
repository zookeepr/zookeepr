import logging
import zookeepr.lib.helpers as h
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from zookeepr.lib.base import BaseController, render

log = logging.getLogger(__name__)

#from zookeepr.lib.base import *
#from zookeepr.lib.auth import SecureController
#from zookeepr.model import Person, DBContent, DBContentType

class HomeController(BaseController):

    def index(self):
        h.flash("Woo, this is pretty")
        h.flash("Woo, this is pretty", 'cat2')
        h.flash("Woo, this is prettyasdf asdf asdf asdf lkasdhf kjlashdflkj hasdlf", 'cat3')
        h.flash("Woo, this is pretadsty", 'cat4')
        h.flash("Woo, this is pretty")
        h.flash("Woo, this is pretadsty", 'error')
        h.flash("Woo, this is pasretty")
        h.flash("Woo, this is asdfpretadsty", 'error')
        h.flash("Woo, this is pretty")
        
        """The home page of the website.

        If the user has not signed in, then they are presented with the
        default page.

        Otherwise, they're shown the customised page.

        We rely on `c.signed_in_person` containing the Person object for
        the currently signed in user, but we don't want to redirect to
        the signin action if we're not signed in so we duplicate the
        __before__ code from SecureController here.
        """

#        if 'signed_in_person_id' in session:
#            c.signed_in_person = self.dbsession.query(Person).filter_by(id=session['signed_in_person_id']).one()
#
#        news = self.dbsession.query(DBContentType).filter_by(name='News').first()
#        if news:
#            setattr(c, 'db_content_news', self.dbsession.query(DBContent).filter_by(type_id=news.id).order_by(DBContent.c.creation_timestamp.desc()).limit(4).all())
#            setattr(c, 'db_content_news_all', self.dbsession.query(DBContent).filter_by(type_id=news.id).order_by(DBContent.c.creation_timestamp.desc()).all())
#
#        press = self.dbsession.query(DBContentType).filter_by(name='In the press').first()
#        if press:
#            setattr(c, 'db_content_press', self.dbsession.query(DBContent).filter_by(type_id=press.id).order_by(DBContent.c.creation_timestamp.desc()).limit(3).all())

        return render('/home.mako')
