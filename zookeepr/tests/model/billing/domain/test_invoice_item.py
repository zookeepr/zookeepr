from zookeepr.tests.model import *

class TestInvoiceItemDomainModel(CRUDModelTest):
    domain = model.billing.InvoiceItem
    samples = [dict(description='desc1',
                    cost=1),
               dict(description='desc2',
                    cost=2),
               ]
