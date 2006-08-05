from zookeepr.tests.model import *

class TestSubmission(ModelTest):
    def test_create(self):
        """Test creation of a Submission object"""
        
        self.model = 'Submission'

        self.check_empty_session()

        session = create_session()

        st = model.SubmissionType(name='BOF')

        # create a person to submit with
        v = model.Person('hacker', 'hacker@example.org',
                         'p4ssw0rd',
                         'E.',
                         'Leet',
                         '+6125555555',
                         )

        print v
        
        session.save(st)
        session.save(v)
        session.flush()

        s = model.Submission(1,
                             'Venal Versimilitude: Vast vocation or violition of volition?',
                             st.id, #FIXME: this exposes knowledge of the table structure to the data model
                             'This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-a-vis an introduction, and so it is my very good honor to meet you and you may call me V.',
                             'Vaudeville',
                             attachment="some attachment",
                             )
        
        # give this sub to v
        v.submissions.append(s)

        session.save(s)
        session.flush()

        vid = v.id
        stid = st.id
        sid = s.id
        
        session.clear()
        
        v = session.get(model.Person, vid)
        s = session.get(model.Submission, sid)
        st = session.get(model.SubmissionType, stid)
        
        self.assertEqual(1, len(v.submissions))
        self.assertEqual(s.title, v.submissions[0].title)
        # check references
        self.assertEqual(v.handle, v.submissions[0].person.handle)
        self.assertEqual(st.name, v.submissions[0].submission_type.name)

        self.assertEqual(buffer("some attachment"), s.attachment)

        # check the submission relations
        self.assertEqual(st.name, s.submission_type.name)
        self.assertEqual(v.handle, s.person.handle)

        print s.submission_type
        print s.person

        session.delete(s)
        session.delete(st)
        session.delete(v)
        session.flush()
        
        v = session.get(model.Person, vid)
        self.failUnlessEqual(None, v)
        s = session.get(model.Submission, sid)
        self.failUnlessEqual(None, s)
        st = session.get(model.SubmissionType, stid)
        self.failUnlessEqual(None, st)
        
        session.close()
        
        self.check_empty_session()
