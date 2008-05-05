from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View
from zookeepr import model
from zookeepr.model import Person
from zookeepr.lib.base import *



class TalkController(BaseController, View):
    model = model.Talk
    individual = 'talk'

    def __before__(self, **kwargs):
        if hasattr(super(BaseController, self), '__before__'):
            super(BaseController, self).__before__(**kwargs)

        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.query(Person).filter_by(id=session['signed_in_person_id']).one()

