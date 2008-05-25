import logging
from formencode import validators, variabledecode
from formencode.schema import Schema
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import BaseSchema, BoundedInt
from zookeepr.lib.base import *
from zookeepr.controllers import not_found

log = logging.getLogger(__name__)

class DbContentSchema(BaseSchema):
    title = validators.String(not_empty=True)
    url = validators.String(not_empty=True)
    body = validators.String(not_empty=True)

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
                   'delete': [AuthRole('organiser')]
                   }

    def page(self):
        url = h.url()()
        if url[0]=='/': url=url[1:]
        c.db_content = self.dbsession.query(model.DBContent).filter_by(url=url).first()
        if c.db_content is not None:
            return render('%s/view.myt' % self.individual)
        return not_found.NotFoundController().view()
        
