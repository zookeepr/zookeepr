from zookeepr.lib.base import *

class SubmissiontypeController(BaseController, View, Modify):
    model = model.SubmissionType
    individual = 'submissiontype'
    conditions = dict(order_by='name')
