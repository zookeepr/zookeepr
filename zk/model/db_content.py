"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from role import Role
from person_role_map import person_role_map

from meta import Session

import datetime
import random

class DbContentType(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'db_content_type'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, nullable=False, unique=True)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(DbContentType, self).__init__(**kwargs)

    def __repr__(self):
        return '<DbContentType id="%s" name="%s">' % (self.id, self.name)

    @classmethod
    def find_by_name(cls, name, abort_404 = True):
        result = Session.query(DbContentType).filter_by(name=name).first()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(DbContentType).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result
        
    @classmethod
    def find_all(cls):
        return Session.query(DbContentType).order_by(DbContentType.id).all()

class DbContent(Base):
    """Stores page information as a baisc CMS.
    """
    __tablename__ = 'db_content'

    id = sa.Column(sa.types.Integer, primary_key=True)
    title = sa.Column(sa.types.Text)
    type_id = sa.Column(sa.types.Integer, sa.ForeignKey('db_content_type.id'))
    url = sa.Column(sa.types.Text)
    body = sa.Column(sa.types.Text)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    publish_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    #relations
    type = sa.orm.relation(DbContentType)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(DbContent, self).__init__(**kwargs)

    def is_news(self):
        news_id = DbContentType.find_by_name("News").id
        if news_id == self.type_id:
            return True
        return False

    def is_page(self):
        news_id = DbContentType.find_by_name("Page").id
        if news_id == self.type_id:
            return True
        return False

    def __repr__(self):
        return '<DbContent id="%s" title="%s" url="%s">' % (self.id, self.title, self.url)

    @classmethod
    def find_by_title(cls, name, about_404 = True):
        result = Session.query(DbContent).filter_by(title=title).filter(DbContent.publish_timestamp <= datetime.datetime.now()).order_by(DbContent.publish_timestamp.desc()).first()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result
        
    @classmethod
    def find_by_url(cls, url, abort_404 = True):
        result = Session.query(DbContent).filter_by(url=url).filter(DbContent.publish_timestamp <= datetime.datetime.now()).order_by(DbContent.publish_timestamp.desc()).first()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(DbContent).filter_by(id=id).order_by(DbContent.publish_timestamp.desc()).first()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result

    @classmethod
    def find_all_by_type_id(cls, type_id, abort_404 = True):
        result = Session.query(DbContent).filter_by(type_id=type_id).filter(DbContent.publish_timestamp <= datetime.datetime.now()).order_by(DbContent.publish_timestamp.desc()).all()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result

    @classmethod
    def find_all_by_type(cls, type, abort_404 = True):
        result = Session.query(DbContent).filter_by(type_id=DbContentType.find_by_name(type, abort_404 = abort_404).id).filter(DbContent.publish_timestamp <= datetime.datetime.now()).order_by(DbContent.publish_timestamp.desc()).all()
        if result is None and abort_404:
            abort(404, "No such db_content object")
        return result
    
    @classmethod
    def find_all(cls):
        return Session.query(DbContent).order_by(DbContent.id).all()

