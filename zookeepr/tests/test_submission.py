import unittest

from sqlalchemy import *
from zookeepr.models import *

class TestSubmission(unittest.TestCase):
    def test_new(self):
        # set up some subtypes
        for n in ['Rock', 'Paper', 'Scissors']:
            ts = SubmissionType.mapper.select_by(name=n)
            if len(ts) == 0:
                SubmissionType(n)

        # create a person to submit with
        v = Person('hacker', 'hacker@example.org',
                   'p4ssw0rd',
                   'E.',
                   'Leet',
                   '+6125555555')

        # all this should just work
        objectstore.commit()

        sub = Submission('Venal Versimilitude: Vast vocation or violition of volition?',
                         SubmissionType.mapper.select_by(name='Paper'),
                         "This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-à-vis an introduction, and so it is my very good honor to meet you and you may call me V.",
                         'Vaudeville',
                         None)
        # give this sub to v
        v.submissions.append(sub)
        
        objectstore.commit()

        assert v.submissions[0].title == 'Venal Versimilitude: Vast vocation or violition of volition?'
        # check references
        assert v.submissions[0].submission_type.name == 'Paper'
        assert v.submissions[0].person.handle == 'hacker'

        # verify that it's in the database?
