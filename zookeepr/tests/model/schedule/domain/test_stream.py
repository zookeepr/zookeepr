from zookeepr.tests.model import ModelTest, model

class TestStreamModel(ModelTest):
    domain = model.schedule.Stream
    samples = [dict(name='Stream 1'),
               dict(name='Stream 2'),
               ]
