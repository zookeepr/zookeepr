from formencode import variabledecode

from zookeepr.lib.auth import AuthRole, SecureController
from zookeepr.lib.base import c, render_response, model
from zookeepr.lib.crud import List, Update, Read
from zookeepr.lib.validators import BaseSchema, ReviewSchema

class EditReviewSchema(BaseSchema):
    review = ReviewSchema()
    pre_validators = [variabledecode.NestedVariables]

class ReviewController(SecureController, List, Update, Read):
    model = model.Review
    individual = 'review'
    permissions = {'index': [AuthRole('reviewer'), AuthRole('organiser')],
                   'edit': [AuthRole('reviewer'), AuthRole('organiser')],
                   'view': [AuthRole('reviewer'), AuthRole('organiser')],
                   'summary': [AuthRole('reviewer'), AuthRole('organiser')]
                   }
    schemas = {'edit': EditReviewSchema(),
               }
    redirect_map = {'edit': dict(controller='review', action='index'),
                    }

    def __before__(self, **kwargs):

        super(ReviewController, self).__before__(**kwargs)

        c.streams = self.dbsession.query(model.Stream).all()


    def summary(self):
        model_name = self.individual
        setattr(c, model_name + '_collection', self.dbsession.query(self.model).select(order_by=self.model.c.id))
        return render_response('review/summary.myt')
