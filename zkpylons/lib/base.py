"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import request, response, session, tmpl_context as c

from zkpylons.model.db_content import DbContent, DbContentType
from zkpylons.model.config import Config
from zkpylons.model import meta
import zkpylons.lib.helpers as h
import datetime

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        person = h.signed_in_person()
        if person and not person.activated:
            msg = ("Your account (%s) hasn't been confirmed. Check your email"
                   " for activation instructions." %
                   (person.email_address))
            h.flash(msg, category="warning")

        # Moved here from index controller so that all views that import the news.mako template
        # have access to c.db_content_news and c.db_content_press
        news = DbContentType.find_by_name("News", abort_404 = False)
        if news:
            c.db_content_news = meta.Session.query(DbContent).filter_by(type_id=news.id).filter(DbContent.publish_timestamp <= datetime.datetime.now()).order_by(DbContent.creation_timestamp.desc()).limit(4).all()
            c.db_content_news_all = meta.Session.query(DbContent).filter_by(type_id=news.id).filter(DbContent.publish_timestamp <= datetime.datetime.now()).order_by(DbContent.creation_timestamp.desc()).all() #use all to find featured items

        press = DbContentType.find_by_name("In the press", abort_404 = False)
        if press:
            c.db_content_press = meta.Session.query(DbContent).filter_by(type_id=press.id).order_by(DbContent.creation_timestamp.desc()).filter(DbContent.publish_timestamp <= datetime.datetime.now()).limit(4).all()

	banner = DbContentType.find_by_name("Banner", abort_404 = False)
        if banner:
                c.db_content_banner = meta.Session.query(DbContent).filter_by(type_id=banner.id).order_by(DbContent.creation_timestamp.desc()).filter(DbContent.publish_timestamp <= datetime.datetime.now()).limit(5).all()

        # Allow direct model query by view using c.config.get("key")
        # This is because with have huge numbers of parameters which can be fetched
        c.config = Config

        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
