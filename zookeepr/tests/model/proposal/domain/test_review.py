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
        self.dbsession.save(self.proposal)

        self.reviewer = model.Person(firstname='snuh', lastname='snuh2', email_address='reviewer@example.org')
        self.dbsession.save(self.reviewer)

        self.stream = model.Stream(name="foo")
        self.dbsession.save(self.stream)

        self.dbsession.flush()

        self.pid = self.proposal.id
        self.rid = self.reviewer.id
        self.sid = self.stream.id

    def tearDown(self):
        self.dbsession.delete(self.dbsession.query(model.Stream).get(self.sid))
        self.dbsession.delete(self.dbsession.query(model.Proposal).get(self.pid))
        self.dbsession.delete(self.dbsession.query(model.Person).get(self.rid))
        self.dbsession.flush()

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
        self.dbsession.save(pt)
        p = model.Proposal(title='proposal',
                           type=pt.id,
                           )
        self.dbsession.save(p)
        s = model.Stream('streamy')
        self.dbsession.save(s)
        r = model.Person(firstname='testguy',
                         lastname='mctest',
                         email_address='testguy@example.org',
                         )
        self.dbsession.save(r)

        self.dbsession.flush()

        # create a review
        r1 = model.Review(reviewer=r,
                          familiarity=1,
                          technical=1,
                          coolness=1,
                          stream=s,
                          )
        self.dbsession.save(r1)
        p.reviews.append(r1)
        self.dbsession.flush()

        # create a second, identical
        r2 = model.Review(reviewer=r,
                          familiarity=1,
                          technical=1,
                          coolness=1,
                          stream=s,
                          )
        self.dbsession.save(r2)
        p.reviews.append(r2)
        # raise an exception when trying to commit this
        self.assertRaises(sqlalchemy.exceptions.SQLError,
                          self.dbsession.flush)

        # clean up
        #self.dbsession.clear()
        self.dbsession.delete(r)
        self.dbsession.delete(s)
        self.dbsession.delete(p)
        self.dbsession.delete(pt)
        self.dbsession.flush()
