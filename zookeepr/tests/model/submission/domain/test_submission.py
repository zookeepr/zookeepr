from zookeepr.tests.model import *

class TestSubmission(ModelTest):
        
    def test_create(self):
        self.model = 'submission.Submission'

        self.check_empty_session()

        session = create_session()

        st = model.submission.SubmissionType(name='BOF')

        # create a person to submit with
        v = model.core.Person('hacker', 'hacker@example.org',
                         'p4ssw0rd',
                         'E.',
                         'Leet',
                         '+6125555555',
                         )

        print v
        
        session.save(st)
        session.save(v)
        session.flush()

        s = model.submission.Submission(title='Venal Versimilitude: Vast vocation or violition of volition?',
                             type=st,
                             abstract='This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-a-vis an introduction, and so it is my very good honor to meet you and you may call me V.',
                             experience='Vaudeville',
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
        
        v = session.get(model.core.Person, vid)
        s = session.get(model.submission.Submission, sid)
        st = session.get(model.submission.SubmissionType, stid)
        
        self.assertEqual(1, len(v.submissions))
        self.assertEqual(s.title, v.submissions[0].title)
        # check references
        self.assertEqual(v, v.submissions[0].people[0])
        self.assertEqual(v.handle, v.submissions[0].people[0].handle)
        self.assertEqual(st.name, v.submissions[0].type.name)

        self.assertEqual(buffer("some attachment"), s.attachment)

        # check the submission relations
        self.assertEqual(st.name, s.type.name)
        self.assertEqual(v.handle, s.people[0].handle)

        print s.type
        print s.people[0]

        session.delete(s)
        session.delete(st)
        session.delete(v)
        session.flush()
        
        v = session.get(model.core.Person, vid)
        self.failUnlessEqual(None, v)
        s = session.get(model.submission.Submission, sid)
        self.failUnlessEqual(None, s)
        st = session.get(model.submission.SubmissionType, stid)
        self.failUnlessEqual(None, st)
        
        session.close()
        
        self.check_empty_session()


    def test_double_person_submission_mapping(self):
        session = create_session()

        r1 = model.core.Person(email_address='testguy@example.org',
                                password='p')
        r2 = model.core.Person(email_address='testgirl@example.com',
                                password='q')
        st = model.submission.SubmissionType('Presentation')

        session.save(r1)
        session.save(r2)
        session.save(st)
        session.flush()
        
        s1 = model.submission.Submission(title='one',
                              abstract='bar',
                              type=st)
        session.save(s1)

        r1.submissions.append(s1)
        # FIXME: this flush blows things up!
        #session.flush()

        self.failUnless(s1 in r1.submissions)

        s2 = model.submission.Submission(title='two',
                              abstract='some abstract',
                              type=st)
        session.save(s2)

        r2.submissions.append(s2)
        session.flush()

        self.failUnless(s2 in r2.submissions)

        print "r1", r1, r1.submissions

        print "r2", r2, r2.submissions

        session.flush()

        # assert positives
        self.failUnless(s1 in r1.submissions)
        self.failUnless(s2 in r2.submissions)

        # now make sure the converse is true
        self.failIf(s1 in r2.submissions, "invalid submission in r2.submissions: %r" % s1)
        self.failIf(s2 in r1.submissions, "invalid submission in r1.submissions: %r" % s2)

        # clean up
        session.delete(s2)
        session.delete(s1)
        session.delete(r2)
        session.delete(r1)
        session.delete(st)
        session.flush()

        # check
        self.model = 'submission.Submission'
        self.check_empty_session()

    def test_multiple_persons_per_submission(self):
        session = create_session()

        p1 = model.core.Person(email_address='one@example.org',
            password='foo')
        st = model.submission.SubmissionType('Presentation')
        session.save(p1)
        session.save(st)
        session.flush()
        s = model.submission.Submission(title='a sub')
        p1.submissions.append(s)
        session.save(s)
        session.flush()

        p2 = model.core.Person(email_address='two@example.org',
            password='bar')
        s.people.append(p2)

        session.save(p2)
        session.flush()

        p3 = model.core.Person(email_address='three@example.org',
            password='quux')
        session.save(p3)
        session.flush()

        self.failUnless(s in p1.submissions)
        self.failUnless(s in p2.submissions)

        self.failUnless(p1 in s.people)
        self.failUnless(p2 in s.people)

        print "p3 subs:", p3.submissions
        print "s.peopl", s.people
        self.failIf(s in p3.submissions)
        self.failIf(p3 in s.people)

        # clean up
        session.delete(s)
        session.delete(p1)
        session.delete(p2)
        session.delete(st)
        session.flush()

        # check
        self.model = 'submission.Submission'
        self.check_empty_session()
