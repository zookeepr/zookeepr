import sqlalchemy.exceptions

from zookeepr.tests.model import ModelTest, model

class TestReviewModel(ModelTest):
#    domain = model.Review
#    samples = [dict(proposal

    def test_one_review_per_reviewer_per_proposal(self):
        """Test that reviewers can only review each proposal once"""
        # set up the bomb
        pt = model.ProposalType('miniconf')
        self.objectstore.save(pt)
        p = model.Proposal(title='proposal',
                           type=pt.id,
                           )
        self.objectstore.save(p)
        s = model.Stream('streamy')
        self.objectstore.save(s)
        r = model.Person(fullname='testguy mctest',
                         email_address='testguy@example.org',
                         )
        self.objectstore.save(r)

        self.objectstore.flush()

        # create a review
        r1 = model.Review(reviewer=r,
                          familiarity=1,
                          technical=1,
                          coolness=1,
                          stream=s,
                          )
        self.objectstore.save(r1)
        p.reviews.append(r1)
        self.objectstore.flush()

        # create a second, identical
        r2 = model.Review(reviewer=r,
                          familiarity=1,
                          technical=1,
                          coolness=1,
                          stream=s,
                          )
        self.objectstore.save(r2)
        p.reviews.append(r2)
        # raise an exception when trying to commit this
        self.assertRaises(sqlalchemy.exceptions.SQLError,
                          self.objectstore.flush)

        # clean up
        #self.objectstore.clear()
        self.objectstore.delete(r)
        self.objectstore.delete(s)
        self.objectstore.delete(p)
        self.objectstore.delete(pt)
        self.objectstore.flush()
