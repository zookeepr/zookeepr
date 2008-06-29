from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController
from zookeepr.model import Person, DBContent, DBContentType

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
        
        news_id = self.dbsession.query(DBContentType).filter_by(name='News').first().id
        setattr(c, 'db_content_news', self.dbsession.query(DBContent).filter_by(type_id=news_id).order_by(DBContent.c.creation_timestamp.desc()).limit(20).all())
        press_id = self.dbsession.query(DBContentType).filter_by(name='In the press').first().id
        setattr(c, 'db_content_press', self.dbsession.query(DBContent).filter_by(type_id=press_id).order_by(DBContent.c.creation_timestamp.desc()).limit(20).all())

        resp = render_response('home.myt')

        return resp
