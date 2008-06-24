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
                   'list_press': True
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
        setattr(c, self.individual + '_collection', self.dbsession.query(self.model).filter_by(type_id=news_id).order_by(self.model.c.id).all())
        return render_response('%s/list_news.myt' % self.individual)
        
    def list_press(self):
        press_id = self.dbsession.query(model.DBContentType).filter_by(name='In the press').first().id
        setattr(c, self.individual + '_collection', self.dbsession.query(self.model).filter_by(type_id=press_id).order_by(self.model.c.id).all())
        return render_response('%s/list_press.myt' % self.individual)

