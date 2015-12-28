from .crud_helper import CrudHelper
from .fixtures import VoucherFactory, CompletePersonFactory, ProductCategoryFactory, ProductFactory, RegistrationFactory

class TestVoucher(CrudHelper):
    def test_permissions(self, app, db_session):
        # index only requires valid user
        # No view or edit page
        CrudHelper.test_permissions(self, app, db_session, get_pages = ('new', 'delete'), post_pages = ('new', 'delete'))
        CrudHelper.test_permissions(self, app, db_session, bad_roles = ['public'], get_pages = ['index'], post_pages = [])

    def test_new(self, app, db_session):
        VoucherFactory()
        peeps = [CompletePersonFactory() for i in range(10)]
        pcats = [ProductCategoryFactory() for i in range(10)]
        db_session.commit()
        prods = [ProductFactory(category=cat, cost=i) for cat in pcats for i in range(10)]
        db_session.commit()

        # Voucher creates a voucher-product entry for each product
        # We don't verify every voucher-product, we just check the count
        count = len([c for c in pcats if c.display == 'radio'])
        count += sum([c.products_nonfree.count() for c in pcats if c.display != 'radio'])

        data = {
                "voucher.leader"  : peeps[6].id,
                "voucher.code"    : "billy",
                "voucher.comment" : "Bill needs a new pair of shoes",
               }

        # A voucher is generated for each count value
        # Values other than one upset the crud DB num-added checker
        data["voucher.count"] = "1"

        for p in prods:
            if p.category.display == 'radio': continue
            if p.cost == 0: continue
            data["products.product_%i_qty" % p.id] = 12
            data["products.product_%i_percentage" % p.id] = 56
        for c in pcats:
            if c.display != 'radio': continue
            data["products.category_%i" % c.id] = c.products[7].id
            data["products.category_%i_percentage" % c.id] = 77

        for c in pcats:
            if c.display != 'radio': continue

        def data_check(new):
            assert new.leader_id == data["voucher.leader"]
            assert new.code.startswith(data["voucher.code"])
            assert new.comment == data["voucher.comment"]

            assert len(new.products) == count

        CrudHelper.test_new(self, app, db_session, form_prefix="", data=data, title="Add a voucher code", do_data_check=False, extra_data_check=data_check)

    def test_view(self):
        # No view page
        pass

    def test_index(self, app, db_session):
        groups = [VoucherFactory(leader=CompletePersonFactory()) for i in range(10)]
        db_session.commit()
        entries = { s.id : [s.code, s.leader.fullname, s.leader.email_address] for s in groups }

        CrudHelper.test_index(self, app, db_session, entries = entries, title="Voucher Codes", entry_actions = ('delete',))

    def test_edit(self):
        # No edit page
        pass

    def test_delete(self, app, db_session):
        CrudHelper.test_delete(self, app, db_session)

        # Can't delete vouchers which have been used - have a rego attached
        target = VoucherFactory()
        rego = RegistrationFactory()
        db_session.commit()
        # TODO: Running rego.voucher = target, or variants, triggers an update that sets code to Null
        #       This then causes a sql constraint violation and errors ensue
        rego.voucher_code = target.code

        try:
            CrudHelper.test_delete(self, app, db_session, target=target)
        except AssertionError as e:
            print e
        else:
            assert False, "Delete should fail if the voucher has an associated registration"
