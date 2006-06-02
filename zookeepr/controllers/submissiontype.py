from zookeepr.lib.auth import SecureController
from zookeepr.lib.base import *

#class SubmissiontypeController(BaseController, SecureController, View, Modify):
class SubmissiontypeController(BaseController, View, Modify):
    model = model.SubmissionType
    individual = 'submissiontype'
    conditions = dict(order_by='name')
