from zookeepr.tests.functional import *

class TestReviewController(SignedInControllerTest):

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
        self.objectstore.save(p1)
        p2 = model.Person(email_address='t2@example.org',
                    fullname='submitter')
        self.objectstore.save(p2)
        p = model.Proposal(title='prop',
                           type=self.objectstore.get(model.ProposalType, 1),
                           )
        self.objectstore.save(p)
        p.people.append(p2)
        r1 = model.Review(
                    reviewer=self.person,
                    familiarity=0,
                    technical=1,
                    experience=1,
                    coolness=1,
                    stream=self.objectstore.get(model.Stream, 1),
                    )
        p.reviews.append(r1)
        self.objectstore.save(r1)
        r2 = model.Review(
                    reviewer=p1,
                    familiarity=1,
                    technical=2,
                    experience=2,
                    coolness=3,
                    stream=self.objectstore.get(model.Stream, 1),
                    )
        p.reviews.append(r2)
        self.objectstore.save(r2)
        self.objectstore.flush()

        resp = self.app.get('/review')
        resp.mustcontain(self.person.firstname)
        self.failIf(p1.firstname in resp, "shouldn't be able to see other people's reviews")


        # clean up
        self.objectstore.delete(p)
        self.objectstore.delete(p1)
        self.objectstore.delete(p2)
        self.objectstore.flush()

#     def test_reviewer_name_hidden_from_submitter(self):
#         """Test taht a revier is anonymouse to submitters"""
#         self.fail("untested")

#     def test_reviewer_cant_review_own_proposal(self):
#         """Test that a reviewer can't review their own submissions."""
#         self.fail("untedted")


