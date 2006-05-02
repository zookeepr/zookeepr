# import unittest

# from sqlalchemy import *
# from zookeepr.models import *

# class TestSubmission(unittest.TestCase):
#     def test_create(self):
#         """Test creation of a Submission object"""
#         # set up some subtypes
#         st = SubmissionType(name='BOF')

#         # create a person to submit with
#         v = Person('hacker', 'hacker@example.org',
#                    'p4ssw0rd',
#                    'E.',
#                    'Leet',
#                    '+6125555555')

#         # all this should just work
#         objectstore.commit()

#         s = Submission('Venal Versimilitude: Vast vocation or violition of volition?',
#                        st,
#                        'This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-a-vis an introduction, and so it is my very good honor to meet you and you may call me V.',
#                        'Vaudeville',
#                        None)
#         # give this sub to v
#         v.submissions.append(s)
        
#         objectstore.commit()

#         assert len(v.submissions) == 1

#         assert v.submissions[0].title == s.title
#         # check references
#         assert v.submissions[0].person.handle == v.handle

#         assert v.submissions[0].submission_type.name == st.name

#         # verify that it's in the database?

#         # clean up
#         sid = s.id
#         vid = v.id
#         stid = st.id

#         s.delete()
#         st.delete()
#         v.delete()
        
#         objectstore.commit()

#         # clean up
#         s = Submission.get(sid)
#         self.failUnless(s is None, "submission still in database")
#         v = Person.get(vid)
#         self.failUnless(v is None, "person still in database")
#         st = SubmissionType.get(stid)
#         self.failUnless(st is None, "subtype still in database")
#         # check
#         ss = Submission.select()
#         self.failUnless(len(ss) == 0, "submission table not empty")
#         sts = SubmissionType.select()
#         self.failUnless(len(sts) == 0, "submission_type table not empty")
#         ps = Person.select()
#         self.failUnless(len(ps) == 0, "person table not empty")
