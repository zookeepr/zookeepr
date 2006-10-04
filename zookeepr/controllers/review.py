from formencode import variabledecode

from zookeepr.lib.auth import AuthRole, SecureController
from zookeepr.lib.base import c, render_response, model, Query
from zookeepr.lib.crud import List, Update
from zookeepr.lib.validators import BaseSchema, ReviewSchema

class EditReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [variabledecode.NestedVariables]

class ReviewController(SecureController, List, Update):
    model = model.Review
    individual = 'review'
    permissions = {'index': [AuthRole('reviewer')],
                   'edit': [AuthRole('reviewer')],
                   }
    schemas = {'edit': EditReviewSchema(),
               }
    redirect_map = {'edit': dict(controller='review', action='index'),
                    }

    def __before__(self, **kwargs):
        
        super(ReviewController, self).__before__(**kwargs)

        c.streams = Query(model.Stream).select()
