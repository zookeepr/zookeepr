from zookeepr.model import Submission, SubmissionType, Person
from zookeepr.tests.model import *

class TestSubmission(ModelTest):
        
    def test_create(self):
        self.model = 'Submission'

        self.check_empty_session()

        st = SubmissionType(name='BOF')

        # create a person to submit with
        v = Person('hacker', 'hacker@example.org',
                   'p4ssw0rd',
                   'E.',
                   'Leet',
                   '+6125555555',
                   )

        print v

        st.save()
        st.flush()
        v.save()
        v.flush()

        s = Submission(title='Venal Versimilitude: Vast vocation or violition of volition?',
                       type=st,
                       abstract='This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-a-vis an introduction, and so it is my very good honor to meet you and you may call me V.',
                       experience='Vaudeville',
                       attachment="some attachment",
                       )
        
        # give this sub to v
        v.submissions.append(s)

        s.save()
        s.flush()

        vid = v.id
        stid = st.id
        sid = s.id

        objectstore.clear()

        print vid, stid, sid

        v = Person.get(vid)
        st = SubmissionType.get(stid)
        s = Submission.get(sid)
        
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

        s.delete()
        s.flush()
        st.delete()
        st.flush()
        v.delete()
        v.flush()
        
        v = Person.get(vid)
        self.failUnlessEqual(None, v)
        s = Submission.get(sid)
        self.failUnlessEqual(None, s)
        st = SubmissionType.get(stid)
        self.failUnlessEqual(None, st)
        
        self.check_empty_session()


    def test_double_person_submission_mapping(self):
        r1 = Person(email_address='testguy@example.org',
                    password='p')
        r2 = Person(email_address='testgirl@example.com',
                    password='q')
        st = SubmissionType('Presentation')

        r1.save()
        r1.flush()
        r2.save()
        r2.flush()
        st.save()
        st.flush()
        
        s1 = Submission(title='one',
                        abstract='bar',
                        type=st)
        s1.save()

        r1.submissions.append(s1)
        s1.flush()

        self.failUnless(s1 in r1.submissions)

        s2 = Submission(title='two',
                        abstract='some abstract',
                        type=st)

        s2.save()
        r2.submissions.append(s2)
        s2.flush()

        self.failUnless(s2 in r2.submissions)

        print "r1", r1, r1.submissions

        print "r2", r2, r2.submissions

        # assert positives
        self.failUnless(s1 in r1.submissions)
        self.failUnless(s2 in r2.submissions)

        # now make sure the converse is true
        self.failIf(s1 in r2.submissions, "invalid submission in r2.submissions: %r" % s1)
        self.failIf(s2 in r1.submissions, "invalid submission in r1.submissions: %r" % s2)

        # clean up
        s2.delete()
        s2.flush()
        s1.delete()
        s1.flush()
        r2.delete()
        r2.flush()
        r1.delete()
        r1.flush()
        st.delete()
        st.flush()

        # check
        self.model = 'Submission'
        self.check_empty_session()

    def test_multiple_persons_per_submission(self):
        p1 = Person(email_address='one@example.org',
                    password='foo')
        st = SubmissionType('Presentation')
        p1.save()
        p1.flush()
        st.save()
        st.flush()

        s = Submission(title='a sub')
        p1.submissions.append(s)
        s.save()
        s.flush()

        p2 = Person(email_address='two@example.org',
                    password='bar')
        s.people.append(p2)
        p2.save()
        p2.flush()

        p3 = Person(email_address='three@example.org',
                    password='quux')
        p3.save()
        p3.flush()

        self.failUnless(s in p1.submissions)
        self.failUnless(s in p2.submissions)

        self.failUnless(p1 in s.people)
        self.failUnless(p2 in s.people)

        print "p3 subs:", p3.submissions
        print "s.people:", s.people
        self.failIf(s in p3.submissions)
        self.failIf(p3 in s.people)

        # clean up
        s.delete()
        s.flush()
        p1.delete()
        p1.flush()
        p2.delete()
        p2.flush()
        st.delete()
        st.flush()

        # check
        self.model = 'Submission'
        self.check_empty_session()
