import logging
import zookeepr.lib.helpers as h
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from zookeepr.model import meta
from zookeepr.model.db_content import DbContent, DbContentType

from zookeepr.lib.base import BaseController, render

log = logging.getLogger(__name__)


class HomeController(BaseController):

    def index(self):
        """The home page of the website.

        If the user has not signed in, then they are presented with the
        default page.

        Otherwise, they're shown the customised page.

        We rely on `c.signed_in_person` containing the Person object for
        the currently signed in user, but we don't want to redirect to
        the signin action if we're not signed in so we duplicate the
        __before__ code from SecureController here.
        """

        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.query(Person).filter_by(id=session['signed_in_person_id']).one()

        news = DbContentType.find_by_name("News", abort_404 = False)
        if news:
            c.db_content_news = meta.Session.query(DbContent).filter_by(type_id=news.id).order_by(DbContent.creation_timestamp.desc()).limit(4).all()
            c.db_content_news_all = meta.Session.query(DbContent).filter_by(type_id=news.id).order_by(DbContent.creation_timestamp.desc()).all() #use all to find featured items

        press = DbContentType.find_by_name("In the press", abort_404 = False)
        if press:
            c.db_content_press = meta.Session.query(DbContent).filter_by(type_id=press.id).order_by(DbContent.creation_timestamp.desc()).limit(4).all()


        return render('/home.mako')
