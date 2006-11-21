import hmac, sha
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *

class InvoiceController(SecureController, Read):
    model = model.Invoice
    individual = 'invoice'
    permissions = {'view': [AuthFunc('is_payee')],
                   }

    def is_payee(self):
        return c.signed_in_person == self.obj.person

    def verify(self):

        # Support GET or POST
        fields = dict(request.POST)
        if 'MAC' not in fields:
            fields = dict(request.GET)


        # If we don't have a valid MAC then we just throw everything away
        # Since someone is being evil
        valid_mac = self.verify_hmac(fields)
        if not valid_mac:
            redirect_to('/Errors/InvalidPayment')

        # TODO Add some field validation
        # I'm just trusting commsecure to do the right thing at the moment

        # Store the payment attempt
        payment_received = model.PaymentReceived()
        payment_received.map_fields(fields)
        self.dbsession.save(payment_received)
        self.dbsession.flush()


        redirect_to('/ShouldntGetHere')


    def verify_hmac(self, fields):
        merchantid =  request.environ['paste.config']['app_conf'].get('commsecure_merchantid')
        secret =  request.environ['paste.config']['app_conf'].get('commsecure_secret')

        # Check for MAC
        if 'MAC' not in fields:
            return False

        # Generate the MAC
        keys = fields.keys()
        keys.sort()
        stringToMAC = '&'.join(['%s=%s' % (key, fields[key]) for key in keys if key != 'MAC'])
        mac = hmac.new(secret, stringToMAC, sha).hexdigest()

        # Check the MAC
        if mac.lower() == fields['MAC'].lower():
            return True

        return False




class PaymentOptions:
    def __init__(self):
        types = {
                "Professional": [51750, 69000],
                "Hobbyist": [30000, 22500],
                "Concession": [9900, 9900]
                }
        dinner = {
                "1": 6000,
                "2": 12000,
                "3": 18000
                }
        accommodation = {
                "0": 0,
                "1": 4950,
                "2": 5500,
                "3": 6000,
                "5": 3500,
                "6": 5850
                }
        ebdate = [22, 11, 06]
        #indates = [14, 15, 16, 17, 18, 19]
        #outdates = [15, 16, 17, 18, 19, 20]
        
        partners = { 
                "0": 0,
                "1": 20000, # just a partner
                "2": 30000, # now the kids
                "3": 40000,
                "4": 50000
                }

    def getTypeAmount(self, type, date):
        if type in types.keys():
            date = [date[:2], date[2:4], date[4:6]]
            if date[2] <= ebdate[2] and date[1] <= ebdate[1] and date[0] <= ebdate[0]:
                return types[type][0]
            else:
                return types[type][1]

    def getDinnerAmount(self, tickets):
        dinnerAmount = dinner[tickets]
        return dinnerAmount

    def getAccommodationRate(self, choice):
        accommodationRate = accommodation[choice]
        return accommodationRate

    def getAccommodationAmount(self, rate, indate, outdate):
        accommodationAmount = (outdate - indate) * rate
        return accommodationAmount 

    def getPartnersAmount(self, partner, kids)
        partnersAmount = partners[partner + kids]
        return partnersAmount


total = 0
total += p.getTypeAmount()
total += p.getDinnerAmount()
total += p.getAccommodationRate()
total += p.getAccommodationAmount()
total += p.getPartnersAmount()
