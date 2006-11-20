from formencode import variabledecode

from zookeepr.lib.auth import AuthRole, SecureController
from zookeepr.lib.base import c, render_response, model, self.dbsession.query
from zookeepr.lib.crud import List, Update, Read
from zookeepr.lib.validators import BaseSchema, ReviewSchema

class EditReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [variabledecode.NestedVariables]

class ReviewController(SecureController, List, Update, Read):
    model = model.Review
    individual = 'review'
    permissions = {'index': [AuthRole('reviewer')],
                   'edit': [AuthRole('reviewer')],
                   'view': [AuthRole('reviewer'), AuthRole('organiser')]
                   }
    schemas = {'edit': EditReviewSchema(),
               }
    redirect_map = {'edit': dict(controller='review', action='index'),
                    }

    def __before__(self, **kwargs):
        
        super(ReviewController, self).__before__(**kwargs)

        c.streams = self.dbsession.query(model.Stream).select()
