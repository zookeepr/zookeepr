from .crud_helper import CrudHelper
from .fixtures import ProductCategoryFactory, FulfilmentTypeFactory, CeilingFactory, ProductFactory

class TestProduct(CrudHelper):
    def test_permissions(self, app, db_session):
        CrudHelper.test_permissions(self, app, db_session)

        # json page requires an organiser or checkin role
        # NOTE: public returns 403 not 401
        bad_roles = ['team', 'reviewer',
                     'miniconf', 'proposals_chair', 'late_submitter',
                     'funding_reviewer', 'press', 'miniconfsonly' ] 
        CrudHelper.test_permissions(self, app, db_session, get_pages=('json',), post_pages=[], bad_roles=bad_roles, good_roles=['organiser'])
        CrudHelper.test_permissions(self, app, db_session, get_pages=('json',), post_pages=[], bad_roles=bad_roles, good_roles=['checkin'])

    def test_new(self, app, db_session):
        categories = [ProductCategoryFactory() for i in range(10)]
        ceilings = [CeilingFactory() for i in range(10)]
        f_types = [FulfilmentTypeFactory() for i in range(10)]
        db_session.commit()

        data = {
                "description"     : "description of the new doll",
                "badge_text"      : "can_haz_dolly",
                "category"        : categories[2].id,
                "fulfilment_type" : f_types[3].id,
                "display_order"   : 23,
                "active"          : True,
                "cost"            : 123456,
                "auth"            : "I have no idea what an auth code is",
                "validate"        : "Is this code that is executed to validate?",
                "ceilings"        : [ceilings[1].id, ceilings[5].id],
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        target = ProductFactory(badge_text="Flubby buddy", auth="Go team!", validate="These are not the droids you are looking for")
        db_session.commit()

        expected = [target.description, target.badge_text, target.category.name, target.fulfilment_type.name, target.display_order, target.cost/100, target.auth, target.validate]
        print expected

        # TODO: These is lots of extra content that should be tested for - sold totals etc.

        CrudHelper.test_view(self, app, db_session, target=target, expected=expected)

    def test_index(self, app, db_session):
        # The index lists categories, not products, which is rather strange
        cats = [ProductCategoryFactory() for i in range(10)]
        db_session.commit()
        entries = { c.id : c.name for c in cats }

        # Disable actions, all the actual links are to categories not product actions

        CrudHelper.test_index(self, app, db_session, entries = entries, entry_actions=[], page_actions=[])

    def test_edit(self, app, db_session):
        categories = [ProductCategoryFactory() for i in range(10)]
        ceilings = [CeilingFactory() for i in range(10)]
        f_types = [FulfilmentTypeFactory() for i in range(10)]
        target = ProductFactory(badge_text="Flubby buddy", auth="Go team!", validate="These are not the droids you are looking for", category=categories[9], fulfilment_type=f_types[5], ceilings=[ceilings[3], ceilings[8]])
        db_session.commit()

        initial_values = {
                "description"     : target.description,
                "badge_text"      : target.badge_text,
                "category"        : str(target.category.id),
                "fulfilment_type" : str(target.fulfilment_type.id),
                "display_order"   : str(target.display_order),
                "active"          : target.active,
                "cost"            : str(target.cost),
                "auth"            : target.auth,
                "validate"        : target.validate,
                "ceilings"        : [str(c.id) for c in target.ceilings],
               }

        new_values = {
                "description"     : "description of the new doll",
                "badge_text"      : "can_haz_dolly",
                "category"        : categories[2].id,
                "fulfilment_type" : f_types[3].id,
                "display_order"   : 23,
                "active"          : True,
                "cost"            : 123456,
                "auth"            : "I have no idea what an auth code is",
                "validate"        : "Is this code that is executed to validate?",
                "ceilings"        : [ceilings[1].id, ceilings[5].id],
               }

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target)
