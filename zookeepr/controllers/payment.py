from zookeepr.lib.base import *
from zookeepr.lib.crud import *

class PaymentController(BaseController, Create):
    """This controller receives payment advice from CommSecure.

    the url /payment/new receives the advice
    """

    domain = model.PaymentReceived
    individual = 'payment'

    def _new_postflush():
        """
   - Verify HMAC (already there)
   - Check the payment ID exists and load it
   - Compare loaded to received to make sure the following match
      * invoiceid
      * amount, orignal_amount

* If something doesn't match then
    * set payments_received.commsecure_status == SHENANIGANS and email
seven-contact
    * set payments.status = FAILED_SHENANIGANS
    * Tell the user something wierd happened and to email seven-contact

* If everything matches
    * set payments_received.commsecure_status == GOOD and email seven-contact

* If payments_received.status == Declined
    * set payments.status = Declined
    * set payments.payments_received_id = payments_received.id
    * Send the user payments_received.ErrorString

* If payments_received.status == Accepted
   * set payments.status = Accepted
   * set payments.payments_received_id = payments_received.id
   * set invoice.status = PAID
   * tell the user ALL GOOD
   """
