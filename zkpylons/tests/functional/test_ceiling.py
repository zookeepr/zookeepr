from routes import url_for

from zk.model import Product

from BeautifulSoup import BeautifulSoup

from .fixtures import CeilingFactory, ProductCategoryFactory, ProductFactory, PersonFactory, RoleFactory, RegistrationFactory, InvoiceFactory, InvoiceItemFactory, CompletePersonFactory
from .utils import do_login
from .crud_helper import CrudHelper

class TestCeiling(CrudHelper):
    def test_new(self, app, db_session):
        cats = [ProductCategoryFactory() for i in range(2)]
        products = [ProductFactory(category=cats[0]) for i in range (4)] \
                 + [ProductFactory(category=cats[1]) for i in range (3)]

        data = {
                'name'            : 'test_new',
                'max_sold'        : '23',
                'available_from'  : '01/02/1945',
                'available_until' : '02/03/1956',
                'products'        : [products[0].id, products[3].id, products[6].id],
               }

        def extra_form_check(form):
            assert len(form.fields['ceiling.products'][0].options) == len(products)

        def extra_data_check(new):
            # Datetime object and multiple products are too complex for the default check
            # So we disable the default data check and replace it with this
            assert new.parent is None
            assert new.name == 'test_new'
            assert new.max_sold == 23
            assert new.available_from.date().isoformat() == '1945-02-01'
            assert new.available_until.date().isoformat() == '1956-03-02'
            selected_ids = data['products']
            assert len(new.products) == len(selected_ids)
            for pid in selected_ids:
                p = Product.find_by_id(pid)
                assert p in new.products

        CrudHelper.test_new(self, app, db_session, data=data, extra_form_check = extra_form_check, do_data_check=False, extra_data_check = extra_data_check)


        # TODO: Invalid content, different date styles

    def test_view(self, app, db_session):
        # These are the number of special people in a given ceiling group
        # Such as number of under 18s or number of special diet folk

        pc1 = ProductCategoryFactory()        
        prods = [ProductFactory(category=pc1) for i in range(2)]
        ceil = CeilingFactory(max_sold=4223, available_from='2012-12-01', available_until='1901-06-23', products=prods)
        peeps = [CompletePersonFactory() for i in range(3)]

        reg1 = RegistrationFactory(person=peeps[0], diet="Wabbits", over18=True)
        reg2 = RegistrationFactory(person=peeps[1], diet="Wrascles", over18=False)
        reg3 = RegistrationFactory(person=peeps[2], diet="", over18=False)

        # need a new invoice item for each invoice
        for peep in peeps:
            InvoiceFactory(person=peep, items=[InvoiceItemFactory(product=p) for p in prods])

        db_session.commit()

        expected = [
                    ceil.name, str(ceil.max_sold),
                    ceil.available_from.strftime("%d/%m/%y"), ceil.available_until.strftime("%d/%m/%y"),
                   ] + [p.description for p in ceil.products]

        resp = CrudHelper.test_view(self, app, db_session, expected=expected, target=ceil)

        print resp
        soup = BeautifulSoup(resp.body)

        def process_table(name):
            table = soup.find(id=name).findNext('table')
            return [row.findAll('td') for row in table.find('tbody').findAll('tr')]

        dietspec_paid = process_table("diet_special_paid")
        assert len(dietspec_paid) == 1
        assert dietspec_paid[0][0].find(text="No entries")

        dietspec_unpaid = process_table("diet_special_invoiced")
        assert len(dietspec_unpaid) == 2
        for pers in [peeps[0], peeps[1]]:
            assert len(filter(None, [c.find(text=pers.fullname) for r in dietspec_unpaid for c in r])) == 1

        diet_paid = process_table("diet_paid")
        assert len(diet_paid) == 1
        assert diet_paid[0][0].find(text="No entries")

        diet_unpaid = process_table("diet_invoiced")
        assert len(diet_unpaid) == 2
        for pers in [peeps[0], peeps[1]]:
            assert len(filter(None, [c.find(text=pers.fullname) for r in diet_unpaid for c in r])) == 1

        u18_paid = process_table("under18_paid")
        assert len(u18_paid) == 1
        assert u18_paid[0][0].find(text="No entries")

        u18_unpaid = process_table("under18_invoiced")
        assert len(u18_unpaid) == 2*2
        for pers in [peeps[1], peeps[2]]:
            assert len(filter(None, [c.find(text=pers.fullname) for r in u18_unpaid for c in r])) == 2

    def test_edit(self, app, db_session):
        cats = [ProductCategoryFactory() for i in range(2)]
        products = [ProductFactory(category=cats[0]) for i in range (4)] \
                 + [ProductFactory(category=cats[1]) for i in range (3)]


        c = CeilingFactory(max_sold=4223, available_from='2012-12-01', available_until='1901-06-23', products=[products[0], products[4], products[1]])

        initial_values = {
            'max_sold'        : str(c.max_sold),
            'available_from'  : '01/12/12',
            'available_until' : '23/06/01',
            'products'        : [str(products[i].id) for i in (0, 1, 4)],
        }

        new_values = {
                'name'            : 'test_new',
                'max_sold'        : '23',
                'available_from'  : '01/02/1945',
                'available_until' : '02/03/1956',
                'products'        : [products[0].id, products[3].id, products[6].id],
               }

        db_session.commit()

        def extra_form_check(form):
            assert len(form.fields['ceiling.products'][0].options) == 7

        def extra_data_check(new):
            # Datetime object and multiple products are too complex for the default check
            # So we disable the default data check and replace it with this
            assert new.parent is None
            assert new.name == 'test_new'
            assert new.max_sold == 23
            assert new.available_from.date().isoformat() == '1945-02-01'
            assert new.available_until.date().isoformat() == '1956-03-02'
            selected_ids = new_values['products']
            assert len(new.products) == len(selected_ids)
            for pid in selected_ids:
                p = Product.find_by_id(pid)
                assert p in new.products

        # TODO: Invalid content, different date styles

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, extra_form_check=extra_form_check, do_data_check=False, extra_data_check=extra_data_check, pageid=c.id)
