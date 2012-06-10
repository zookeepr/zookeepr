from zkpylons.tests.model import TableTest, model

class TestStreamTable(TableTest):
    table = model.schedule.tables.stream
    samples = [dict(name='Deep Hacking'),
               dict(name='Free Love and Open Sensual Stimulation'),
               ]
    not_nullables = ['name']
    uniques = ['name']
