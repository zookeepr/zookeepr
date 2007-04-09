from zookeepr.tests.functional import *

class TestReviewController(SignedInCRUDControllerTest):
#     model = model.Review
#     name = 'review'
#     url = '/review'
#     samples = [dict(comment='a',
#                     familiarity=0,
#                     technical=0,
#                     experience=0,
#                     coolness=0),
#                dict(comment='b',
#                     familiarity=1,
#                     technical=1,
#                     experience=1,
#                     coolness=1)
#                ]

#     def additional(self, obj):
#         obj.stream = self.dbsession.query(model.Stream).get(1)
#         obj.proposal = self.dbsession.query(model.Proposal).get(1)
#         return obj

    def setUp(self):
        super(TestReviewController, self).setUp()

        model.proposal.tables.proposal_type.insert().execute(
            {'id': 1, 'name': 'paper'}
            )
        model.core.tables.role.insert().execute(
            {'id': 1, 'name': 'reviewer'}
            )
        model.core.tables.person_role_map.insert().execute(
            {'person_id': self.person.id, 'role_id': 1}
            )
        model.schedule.tables.stream.insert().execute(
            {'id': 1, 'name': 'streamy'}
            )

    def tearDown(self):
        model.schedule.tables.stream.delete().execute()
        model.core.tables.person_role_map.delete().execute()
        model.core.tables.role.delete().execute()
        model.proposal.tables.proposal_type.delete().execute()
        
        super(TestReviewController, self).tearDown()

#     def test_review_feedback(self):
#         """Test that one can put in optional feedback to the submitter from the review interface.
#         """
#         self.fail("untested")

#     def test_review_interface(self):
#         """Test that the interface shows two lists, one of unreviewed proposals, and one of reviewed proposals"""
#         self.fail("untested")

#     def test_review_interface_sorted(self):
#         """Test that the reviewed proposals are sorted by rank"""
#         self.fail("untested")

    def test_reviews_isolated(self):
        """Test that a reviewer can only see their own reviews"""
        p1 = model.Person(email_address='testgirl@example.org',
                    fullname='Testgirl Van der Test')
        self.dbsession.save(p1)
        p2 = model.Person(email_address='t2@example.org',
                    fullname='submitter')
        self.dbsession.save(p2)
        p = model.Proposal(title='prop',
                           type=self.dbsession.get(model.ProposalType, 1),
                           )
        self.dbsession.save(p)
        p.people.append(p2)
        r1 = model.Review(
                    reviewer=self.person,
                    familiarity=0,
                    technical=1,
                    experience=1,
                    coolness=1,
                    stream=self.dbsession.get(model.Stream, 1),
                    )
        p.reviews.append(r1)
        self.dbsession.save(r1)
        r2 = model.Review(
                    reviewer=p1,
                    familiarity=1,
                    technical=2,
                    experience=2,
                    coolness=3,
                    stream=self.dbsession.get(model.Stream, 1),
                    )
        p.reviews.append(r2)
        self.dbsession.save(r2)
        self.dbsession.flush()
        p1id = p1.id
        p2id = p2.id
        pid = p.id

        resp = self.app.get('/review')
        resp.mustcontain(self.person.fullname)
        self.failIf(p1.fullname in resp, "shouldn't be able to see other people's reviews")
        # clean up
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(pid))
        self.dbsession.delete(self.dbsession.query(model.Person).get(p1id))
        self.dbsession.delete(self.dbsession.query(model.Person).get(p2id))
        self.dbsession.flush()

#     def test_reviewer_name_hidden_from_submitter(self):
#         """Test taht a revier is anonymouse to submitters"""
#         self.fail("untested")

#     def test_reviewer_cant_review_own_proposal(self):
#         """Test that a reviewer can't review their own submissions."""
#         self.fail("untedted")

    def test_only_one_review_per_reviewer_per_proposal(self):
        """test that reviewers can only do one review per proposal"""
        p2 = model.Person(email_address='t2@example.org',
                    fullname='submitter')
        self.dbsession.save(p2)
        p = model.Proposal(title='prop',
                           abstract='abs',
                           experience='exp',
                           type=self.dbsession.get(model.ProposalType, 1),
                           )
        self.dbsession.save(p)
        p.people.append(p2)
        self.dbsession.flush()
        p2id = p2.id
        pid = p.id

        resp = self.app.get(url_for(controller='proposal',
                                    action='review',
                                    id=p.id))
        f = resp.form
        resp = f.submit()

        # do it again 
        resp = f.submit()
        resp.mustcontain("already reviewed this proposal")
        
        # clean up
        self.dbsession.delete(self.dbsession.query(model.Person).get(p2id))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(pid))
        self.dbsession.flush()

    def test_edit_review(self):
        """test that a reviewer can edit their review"""
        s = model.Person(email_address='submitter@example.org',
                         fullname='submitter')
        self.dbsession.save(s)
        p = model.Proposal(title='prop',
                           abstract='abs',
                           experience='exp',
                           type=self.dbsession.query(model.ProposalType).get(1))
        self.dbsession.save(p)
        s.proposals.append(p)
        r = model.Review(reviewer=self.person,
                         familiarity=0,
                         technical=0,
                         experience=0,
                         coolness=0,
                         stream=self.dbsession.query(model.Stream).get(1))
        self.dbsession.save(r)
        p.reviews.append(r)
        self.dbsession.flush()
        sid = s.id
        pid = p.id
        rid = r.id

        # clear the session
        self.dbsession.clear()

        resp = self.app.get(url_for(controller='review',
                                    action='edit',
                                    id=rid))
        f = resp.form
        f['review.comment'] = 'hi!'
        f['review.coolness'] = 1
        resp = f.submit()

        print resp
        

        r = self.dbsession.query(model.Review).get(rid)
        print r
        print r.comment
        self.assertEqual('hi!', r.comment)
        self.assertEqual(1, r.coolness)

        # clean up
        self.dbsession.delete(r)
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(pid))
        self.dbsession.delete(self.dbsession.query(model.Person).get(sid))
        self.dbsession.flush()
