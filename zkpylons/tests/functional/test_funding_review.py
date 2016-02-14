from .crud_helper import CrudHelper
from .fixtures import FulfilmentStatusFactory, FulfilmentTypeFactory, PersonFactory, FulfilmentGroupFactory
from .fixtures import RoleFactory, PersonFactory, CompletePersonFactory, FundingReviewFactory

class TestFundingReview(CrudHelper):
    def test_permissions(self, app, db_session):
        # Edit and delete both require that we own the target
        user = PersonFactory(roles = [RoleFactory(name = 'funding_reviewer')])
        target = FundingReviewFactory(reviewer=user)

        CrudHelper.test_permissions(self, app, db_session, good_pers=user, good_roles = ['funding_reviewer'], target=target, additional_get_pages='summary', dont_get_pages='new', dont_post_pages='new')

    def test_new(self):
        # No new method
        pass

    def test_view(self, app, db_session):
        user = PersonFactory(roles = [RoleFactory(name = 'funding_reviewer')])
        target = FundingReviewFactory()
        db_session.commit()
        expected = [target.reviewer.fullname, str(target.score), target.comment, target.funding.person.fullname]
        CrudHelper.test_view(self, app, db_session, user=user, target=target, expected=expected, title="Funding Review %d" % target.id)

    def test_index(self, app, db_session):
        user = PersonFactory(roles = [RoleFactory(name = 'funding_reviewer')])
        # Only reviews by the viewing user are listed
        reviews = [FundingReviewFactory(reviewer=user) for i in range(10)]
        other_reviews = [FundingReviewFactory() for i in range(10)]
        db_session.commit()
        entries = { s.id : str(s.score) for s in reviews }

        CrudHelper.test_index(self, app, db_session, user=user, entries = entries, title="Your funding reviews", page_actions=[])

    def test_edit(self, app, db_session):
        # Edit requires the logged in person to have created the review
        user = CompletePersonFactory(roles = [RoleFactory(name = 'funding_reviewer')])
        target = FundingReviewFactory(reviewer=user, score=2)
        db_session.commit()

        initial_values = {
                "score"    : "+2",
                "comment"  : target.comment,
                }

        new_values = {
                "score"    : -1,
                "comment"  : "Uncle Uncle",
               }

        CrudHelper.test_edit(self, app, db_session, user=user, initial_values=initial_values, new_values=new_values, pageid=target.id, title="Funding Application Review Update", form_prefix="review")

    def test_delete(self, app, db_session):
        user = CompletePersonFactory(roles = [RoleFactory(name = 'funding_reviewer')])
        target = FundingReviewFactory(reviewer=user, score=2)
        CrudHelper.test_delete(self, app, db_session, user=user, target=target, title="Delete a funding application review")

