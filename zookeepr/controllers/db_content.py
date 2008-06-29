import logging
from formencode import validators, variabledecode
from formencode.schema import Schema
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import BaseSchema, BoundedInt, DbContentTypeValidator
from zookeepr.lib.base import *
from zookeepr.controllers import not_found
from zookeepr.model.db_content import DBContentType

from webhelpers.pagination import paginate

log = logging.getLogger(__name__)

class DbContentSchema(BaseSchema):
    title = validators.String(not_empty=True)
    type = DbContentTypeValidator()
    url = validators.String()
    body = validators.String()

class NewContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [variabledecode.NestedVariables]

class UpdateContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [variabledecode.NestedVariables]


class DbContentController(SecureController, Create, List, Read, Update, Delete):
    individual = 'db_content'
    model = model.DBContent
    schemas = {'new': NewContentSchema(),
               'edit': UpdateContentSchema()
              }

    permissions = {'new': [AuthRole('organiser')],
                   'index': [AuthRole('organiser')],
                   'page': True,
                   'view': True,
                   'edit': [AuthRole('organiser')],
                   'delete': [AuthRole('organiser')],
                   'list_news': True,
                   'list_press': True,
                   'rss_news': True
                   }

    def __before__(self, **kwargs):
        super(DbContentController, self).__before__(**kwargs)
        c.db_content_types = self.dbsession.query(DBContentType).all()

    def view(self):
        news_id = self.dbsession.query(model.DBContentType).filter_by(name='News').first().id
        c.is_news = False
        if news_id == c.db_content.type_id:
            c.is_news = True
        return super(DbContentController, self).view()

    def page(self):
        url = h.url()()
        if url[0]=='/': url=url[1:]
        c.db_content = self.dbsession.query(model.DBContent).filter_by(url=url).first()
        if c.db_content is not None:
            return self.view()
        return not_found.NotFoundController().view()
    
    def list_news(self):
        news_id = self.dbsession.query(model.DBContentType).filter_by(name='News').first().id
        news_list = self.dbsession.query(self.model).filter_by(type_id=news_id).order_by(self.model.c.creation_timestamp.desc()).all()
        pages, collection = paginate(news_list, per_page = 2)
        setattr(c, self.individual + '_pages', pages)
        setattr(c, self.individual + '_collection', collection)
        return render_response('%s/list_news.myt' % self.individual)
    
    def rss_news(self):
        news_id = self.dbsession.query(model.DBContentType).filter_by(name='News').first().id
        news_list = self.dbsession.query(self.model).filter_by(type_id=news_id).order_by(self.model.c.creation_timestamp.desc()).all()
        setattr(c, self.individual + '_collection', news_list)
        return render_response('%s/rss_news.myt' % self.individual, fragment=True)

    def list_press(self):
        press_id = self.dbsession.query(model.DBContentType).filter_by(name='In the press').first().id
        press_list = self.dbsession.query(self.model).filter_by(type_id=press_id).order_by(self.model.c.creation_timestamp.desc()).all()
        pages, collection = paginate(press_list, per_page = 1)
        setattr(c, self.individual + '_pages', pages)
        setattr(c, self.individual + '_collection', collection)
        return render_response('%s/list_press.myt' % self.individual)

