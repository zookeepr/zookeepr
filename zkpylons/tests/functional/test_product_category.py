from .crud_helper import CrudHelper
from .fixtures import ProductCategoryFactory

class TestProductCategory(CrudHelper):
    def test_permissions(self, app, db_session):
        CrudHelper.test_permissions(self, app, db_session, additional_get_pages='stats')

    def test_new(self, app, db_session):
        data = {
                "name"                  : "dinosaurs",
                "description"           : "ancient creatures, some feathery, some good eatin, that roamed the earth",
                "note"                  : "best eatin lightly fried with rice and a little chilli",
                "display"               : "checkbox",
                "display_mode"          : "backwards",
                "display_order"         : 23,
                "invoice_free_products" : True,
                "min_qty"               : 12,
                "max_qty"               : 24,
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        target = ProductCategoryFactory(note='nothing interesting to see here', min_qty=50, max_qty=2300)
        db_session.commit()
        expected = [target.name, target.description, target.note, target.display, target.display_mode, str(target.display_order), str(target.min_qty), str(target.max_qty)]
        print expected

        CrudHelper.test_view(self, app, db_session, target=target, expected=expected)

    def test_index(self, app, db_session):
        groups = [ProductCategoryFactory() for i in range(10)]
        db_session.commit()
        entries = { s.id : s.name for s in groups }

        CrudHelper.test_index(self, app, db_session, entries = entries, title="List of categories")

    def test_edit(self, app, db_session):
        target = ProductCategoryFactory(note='nothing interesting to see here', min_qty=50, max_qty=2300)
        db_session.commit()

        initial_values = {
                "name"                  : target.name,
                "description"           : target.description,
                "note"                  : target.note,
                "display"               : target.display,
                "display_mode"          : target.display_mode,
                "display_order"         : str(target.display_order),
                "invoice_free_products" : target.invoice_free_products,
                "min_qty"               : str(target.min_qty),
                "max_qty"               : str(target.max_qty),
                }

        new_values = {
                "name"                  : "dinosaurs",
                "description"           : "ancient creatures, some feathery, some good eatin, that roamed the earth",
                "note"                  : "best eatin lightly fried with rice and a little chilli",
                "display"               : "checkbox",
                "display_mode"          : "backwards",
                "display_order"         : 23,
                "invoice_free_products" : True,
                "min_qty"               : 12,
                "max_qty"               : 24,
               }

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target, title="Edit Category")

    def test_delete(self, app, db_session):
        CrudHelper.test_delete(self, app, db_session, title="Delete Category")
