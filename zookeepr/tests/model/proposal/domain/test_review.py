import sqlalchemy.exceptions

from zookeepr.tests.model import *

class TestReviewModel(ModelTest):
#    domain = model.Review
#    samples = [dict(proposal

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
