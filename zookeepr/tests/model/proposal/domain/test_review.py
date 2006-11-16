import sqlalchemy.exceptions

from zookeepr.tests.model import *

class TestReviewModel(CRUDModelTest):
    domain = model.Review
    samples = [dict(familiarity=1,
                    technical=1,
                    experience=1,
                    coolness=1,
                    comment="c1",
                    ),
                dict(familiarity=2,
                    technical=2,
                    experience=2,
                    coolness=2,
                    comment="c2",
                    ),
                ]

    def setUp(self):
        super(TestReviewModel, self).setUp()

        self.proposal = model.Proposal(title='p', abstract='a')
        objectstore.save(self.proposal)

        self.reviewer = model.Person(fullname='snuh', email_address='reviewer@example.org')
        objectstore.save(self.reviewer)

        self.stream = model.Stream(name="foo")
        objectstore.save(self.stream)

        objectstore.flush()

        self.pid = self.proposal.id
        self.rid = self.reviewer.id
        self.sid = self.stream.id

    def tearDown(self):
        objectstore.delete(Query(model.Stream).get(self.sid))
        objectstore.delete(Query(model.Proposal).get(self.pid))
        objectstore.delete(Query(model.Person).get(self.rid))
        objectstore.flush()

        super(TestReviewModel, self).tearDown()

    def additional(self, review):
        review.proposal = self.proposal
        review.reviewer = self.reviewer
        review.stream = self.stream
        return review

    def test_one_review_per_reviewer_per_proposal(self):
        """Test that reviewers can only review each proposal once"""
        # set up the bomb
        pt = model.ProposalType('miniconf')
        objectstore.save(pt)
        p = model.Proposal(title='proposal',
                           type=pt.id,
                           )
        objectstore.save(p)
        s = model.Stream('streamy')
        objectstore.save(s)
        r = model.Person(fullname='testguy mctest',
                         email_address='testguy@example.org',
                         )
        objectstore.save(r)

        objectstore.flush()

        # create a review
        r1 = model.Review(reviewer=r,
                          familiarity=1,
                          technical=1,
                          coolness=1,
                          stream=s,
                          )
        objectstore.save(r1)
        p.reviews.append(r1)
        objectstore.flush()

        # create a second, identical
        r2 = model.Review(reviewer=r,
                          familiarity=1,
                          technical=1,
                          coolness=1,
                          stream=s,
                          )
        objectstore.save(r2)
        p.reviews.append(r2)
        # raise an exception when trying to commit this
        self.assertRaises(sqlalchemy.exceptions.SQLError,
                          objectstore.flush)

        # clean up
        #objectstore.clear()
        objectstore.delete(r)
        objectstore.delete(s)
        objectstore.delete(p)
        objectstore.delete(pt)
        objectstore.flush()
