from zookeepr.tests.model import *

class TestStreamModel(CRUDModelTest):
    domain = model.schedule.Stream
    samples = [dict(name='Stream 1'),
               dict(name='Stream 2'),
               ]
