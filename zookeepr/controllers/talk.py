from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View
from zookeepr import model

class TalkController(BaseController, View):
    model = model.Proposal
    individual = 'talk'
