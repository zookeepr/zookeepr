from zookeepr.tests.model import *

class TestStreamTable(TableTest):
    table = model.schedule.tables.stream
    samples = [dict(name='Deep Hacking'),
               dict(name='Free Love and Open Sensual Stimulation'),
               ]
    not_nullable = ['name']
    unique = ['name']
