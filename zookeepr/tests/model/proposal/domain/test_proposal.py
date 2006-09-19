import datetime

from zookeepr.model import Proposal, ProposalType, Person, Attachment, Stream, Review
from zookeepr.tests.model import *

class TestProposal(ModelTest):
        
    def test_create(self):
        self.domain = model.proposal.Proposal

        self.check_empty_session()

        st = ProposalType(name='BOF')

        # create a person to submit with
        v = Person('hacker', 'hacker@example.org',
                   'p4ssw0rd',
                   'E.',
                   'Leet',
                   '+6125555555',
                   )

        print v

        objectstore.save(st)
        objectstore.save(v)
        objectstore.flush()

        s = Proposal(title='Venal Versimilitude: Vast vocation or violition of volition?',
                       type=st,
                       abstract='This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-a-vis an introduction, and so it is my very good honor to meet you and you may call me V.',
                       experience='Vaudeville',
                       )
        
        # give this sub to v
        v.proposals.append(s)

        objectstore.save(s)
        objectstore.flush()

        vid = v.id
        stid = st.id
        sid = s.id

        objectstore.clear()

        print vid, stid, sid

        v = objectstore.get(Person, vid)
        st = objectstore.get(ProposalType, stid)
        s = objectstore.get(Proposal, sid)
        
        self.assertEqual(1, len(v.proposals))
        self.assertEqual(s.title, v.proposals[0].title)
        # check references
        self.assertEqual(v, v.proposals[0].people[0])
        self.assertEqual(v.handle, v.proposals[0].people[0].handle)
        self.assertEqual(st.name, v.proposals[0].type.name)

        # check the proposal relations
        self.assertEqual(st.name, s.type.name)
        self.assertEqual(v.handle, s.people[0].handle)

        print s.type
        print s.people[0]

        objectstore.delete(s)
        objectstore.delete(st)
        objectstore.delete(v)
        objectstore.flush()
        
        v = objectstore.get(Person, vid)
        self.failUnlessEqual(None, v)
        s = objectstore.get(Proposal, sid)
        self.failUnlessEqual(None, s)
        st = objectstore.get(ProposalType, stid)
        self.failUnlessEqual(None, st)
        
        self.check_empty_session()


    def test_double_person_proposal_mapping(self):
        r1 = Person(email_address='testguy@example.org',
                    password='p')
        r2 = Person(email_address='testgirl@example.com',
                    password='q')
        st = ProposalType('Presentation')

        objectstore.save(r1)
        objectstore.save(r2)
        objectstore.save(st)
        
        objectstore.flush()
        
        s1 = Proposal(title='one',
                        abstract='bar',
                        type=st)
        objectstore.save(s1)

        r1.proposals.append(s1)
        objectstore.flush()

        self.failUnless(s1 in r1.proposals)

        s2 = Proposal(title='two',
                        abstract='some abstract',
                        type=st)

        objectstore.save(s2)
        r2.proposals.append(s2)
        objectstore.flush()

        self.failUnless(s2 in r2.proposals)

        print "r1", r1, r1.proposals

        print "r2", r2, r2.proposals

        # assert positives
        self.failUnless(s1 in r1.proposals)
        self.failUnless(s2 in r2.proposals)

        # now make sure the converse is true
        self.failIf(s1 in r2.proposals, "invalid proposal in r2.submissions: %r" % s1)
        self.failIf(s2 in r1.proposals, "invalid proposal in r1.submissions: %r" % s2)

        # clean up
        objectstore.delete(s2)
        objectstore.delete(s1)
        objectstore.delete(r2)
        objectstore.delete(r1)
        objectstore.delete(st)
        objectstore.flush()

        # check
        self.domain = model.proposal.Proposal
        self.check_empty_session()

    def test_multiple_persons_per_proposal(self):
        p1 = Person(email_address='one@example.org',
                    password='foo')
        st = ProposalType('Presentation')
        objectstore.save(p1)
        objectstore.save(st)

        s = Proposal(title='a sub')
        p1.proposals.append(s)
        objectstore.save(s)
        objectstore.flush()

        p2 = Person(email_address='two@example.org',
                    password='bar')
        s.people.append(p2)
        objectstore.save(p2)
        objectstore.flush()

        p3 = Person(email_address='three@example.org',
                    password='quux')
        objectstore.save(p3)
        objectstore.flush()


        self.failUnless(s in p1.proposals)
        self.failUnless(s in p2.proposals)

        self.failUnless(p1 in s.people)
        self.failUnless(p2 in s.people)

        print "p3 subs:", p3.proposals
        print "s.people:", s.people
        self.failIf(s in p3.proposals)
        self.failIf(p3 in s.people)

        # clean up
        objectstore.delete(s)
        objectstore.delete(p1)
        objectstore.delete(p2)
        objectstore.delete(st)

        objectstore.flush()
        
        # check
        self.domain = model.proposal.Proposal
        self.check_empty_session()

    def test_proposal_with_attachment(self):
        p = Proposal(title='prop 1')
        objectstore.save(p)

        a = Attachment(filename='a',
                       content_type='text/plain',
                       creation_timestamp=datetime.datetime.now(),
                       content="foobar")
        objectstore.save(a)

        p.attachments.append(a)
        objectstore.flush()

        pid = p.id
        aid = a.id

        objectstore.clear()

        p = objectstore.get(Proposal, pid)
        a = objectstore.get(Attachment, aid)
        self.assertEqual(p.attachments[0], a)

        objectstore.delete(a)
        objectstore.delete(p)
        objectstore.flush()

        #self.assertEmptyModel(Attachment)
        #self.assertEmptyModel(Proposal)


    def test_reviewed_proposal(self):
        p1 = Person(email_address='one@example.org',
                    password='foo')
        st = ProposalType('Presentation')
        objectstore.save(p1)
        objectstore.save(st)

        s = Proposal(title='a sub')
        p1.proposals.append(s)
        objectstore.save(s)

        p2 = Person(email_address='reviewer@example.org',
                    password='bar')
        objectstore.save(p2)

        stream = Stream(name="pants")

        r = Review(reviewer=p2, stream=stream, comment="Buuzah")
        s.reviews.append(r)
        objectstore.save(r)
        

        objectstore.flush()

        self.failUnless(s in p1.proposals)
        self.failUnless(s not in p2.proposals)

        self.failUnless(p1 in s.people)
        self.failUnless(p2 not in s.people)

        self.failUnless(r in s.reviews)

        # clean up
        objectstore.delete(s)
        objectstore.delete(p1)
        objectstore.delete(p2)
        objectstore.delete(st)
        objectstore.delete(stream)

        objectstore.flush()
        
        # check
        self.domain = model.proposal.Proposal
        self.check_empty_session()
        
