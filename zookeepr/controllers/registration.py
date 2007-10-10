import datetime
import md5
import warnings

from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import *
from zookeepr.lib.mail import *
from zookeepr.lib.validators import BaseSchema, BoundedInt, EmailAddress
from zookeepr.model.registration import Accommodation

class DictSet(validators.Set):
    def _from_python(self, value):
        value = super(DictSet, self)._from_python(value, state)
        return dict(zip(value, [1]*len(value)))
        
    def _to_python(self, value, state):
        value = value.keys()
        return super(DictSet, self)._to_python(value, state)


# FIXME: merge with account.py controller and move to validators
class NotExistingAccountValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        account = state.query(model.Person).get_by(email_address=value['email_address'])
        if account is not None:
            raise Invalid("This account already exists.  Please try signing in first.  Thanks!", value, state)

        account = state.query(model.Person).get_by(handle=value['handle'])
        if account is not None:
            raise Invalid("This display name has been taken, sorry.  Please use another.", value, state)

class SillyDescriptionMD5(validators.FancyValidator):
    def validate_python(self, value, state):
        checksum = md5.new(value['silly_description']).hexdigest()
	if value['silly_description_md5'] != checksum:
	    raise Invalid("Smart enough to hack the silly description, not smart enough to hack the MD5.", value, state)

class NotExistingRegistrationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        rego = None
        if 'signed_in_person_id' in session:
            rego = state.query(model.Registration).get_by(person_id=session['signed_in_person_id'])
        if rego is not None:
            raise Invalid("Thanks for your keenness, but you've already registered!", value, state)

# Only cares about real discount codes
class DuplicateDiscountCodeValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        discount_code = state.query(model.DiscountCode).get_by(code=value['discount_code'])
        if discount_code:
            for r in discount_code.registrations:
                if r.person_id != session['signed_in_person_id']:
                    raise Invalid("Discount code already in use!", value, state)

class SpeakerDiscountValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        if value['type']=='Speaker' or value['accommodation'] in (51,52,53):
	    if 'signed_in_person_id' in session:
		signed_in_person = state.query(model.Person).get_by(id=session['signed_in_person_id'])
		is_speaker = reduce(lambda a, b: a or b.accepted,
					 signed_in_person.proposals, False)
		if not is_speaker:
		    raise Invalid("You don't appear to be a speaker, don't claim a speaker discount.", value, state)
	    else:
		raise Invalid("Please log in before claiming a speaker discount!", value, state)

class AccommodationValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if value == 'own':
            return None
        return state.query(model.Accommodation).get(value)

    def _from_python(self, value):
        return value.id


class RegistrationSchema(Schema):
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    country = validators.String(not_empty=True)
    postcode = validators.String(not_empty=True)

    phone = validators.String()
    
    company = validators.String()
    nick = validators.String()

    shell = validators.String()
    shelltext = validators.String()
    editor = validators.String()
    editortext = validators.String()
    distro = validators.String()
    distrotext = validators.String()
    silly_description = validators.String()
    silly_description_md5 = validators.String(strip=True)

    prevlca = DictSet(if_missing=None)

    type = validators.String(not_empty=True)
    discount_code = validators.String()

    teesize = validators.String(not_empty=True)
    dinner = BoundedInt(min=0)
    diet = validators.String()
    special = validators.String()
    miniconf = DictSet(if_missing=None)
    opendaydrag = BoundedInt(min=0)

    partner_email = EmailAddress(resolve_domain=True)
    kids_0_3 = BoundedInt(min=0)
    kids_4_6 = BoundedInt(min=0)
    kids_7_9 = BoundedInt(min=0)
    kids_10 = BoundedInt(min=0)

    accommodation = AccommodationValidator()
    
    checkin = BoundedInt(min=0)
    checkout = BoundedInt(min=0)

    lasignup = validators.Bool()
    announcesignup = validators.Bool()
    delegatesignup = validators.Bool()

    speaker_record = validators.Bool()
    speaker_video_release = validators.Bool()
    speaker_slides_release = validators.Bool()
    
    chained_validators = [DuplicateDiscountCodeValidator(),
			 SillyDescriptionMD5(), SpeakerDiscountValidator()]

class PersonSchema(Schema):
    email_address = EmailAddress(resolve_domain=True, not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    handle = validators.String(not_empty=True)

    chained_validators = [NotExistingAccountValidator(), validators.FieldsMatch('password', 'password_confirm')]


class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegistrationSchema()

    chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]


class ExistingPersonRegoSchema(BaseSchema):
    registration = RegistrationSchema()

    chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]


class EditRegistrationSchema(BaseSchema):
    registration = RegistrationSchema()

    #chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]


class RegistrationController(BaseController, Create, Update, List):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               'edit': EditRegistrationSchema(),
               }
    redirect_map = {'edit': dict(controller='registration', action='status'),
                    }
    permissions = { 'remind': [AuthRole('organiser')],
                    'list': [AuthRole('organiser')],
                   }
    anon_actions = ['status']

    def is_same_person(self):
        return c.signed_in_person == c.registration.person

    def __before__(self, **kwargs):
        if hasattr(super(RegistrationController, self), '__before__'):
            super(RegistrationController, self).__before__(**kwargs)

        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.query(model.Person).get_by(id=session['signed_in_person_id'])
	    is_speaker = reduce(lambda a, b: a or b.accepted,
				       c.signed_in_person.proposals, False)
        else:
	    is_speaker = False

        as = self.dbsession.query(model.Accommodation).select()
	def space_available(a):
	  if is_speaker and a.name=='Trinity':
	    return True
	  return a.get_available_beds() >= 1
        c.accommodation_collection = filter(space_available, as)
	c.accommodation_collection.sort(cmp = lambda a, b: cmp(a.id, b.id))

    def edit(self, id):
        if not self.is_same_person() and not AuthRole('organiser').authorise(self):
            abort(403)

        registration = self.obj
        if registration.person.invoices:
            if registration.person.invoices[0].good_payments or registration.person.invoices[0].bad_payments:
                redirect_to("/Errors/InvoiceAlreadyPaid")

        return super(RegistrationController, self).edit(id)

    def new(self):
        errors = {}
        defaults = dict(request.POST)

        if defaults:
            if c.signed_in_person:
                results, errors = ExistingPersonRegoSchema().validate(defaults, self.dbsession)
            else:
                results, errors = NewRegistrationSchema().validate(defaults, self.dbsession)

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
                c.registration = model.Registration()
                for k in results['registration']:
                    setattr(c.registration, k, results['registration'][k])
                self.dbsession.save(c.registration)

                if not c.signed_in_person:
                    c.person = model.Person()
                    for k in results['person']:
                        setattr(c.person, k, results['person'][k])

                    self.dbsession.save(c.person)
                else:
                    c.person = c.signed_in_person

                c.registration.person = c.person
                self.dbsession.flush()

		email(
		    c.person.email_address,
		    render('registration/response.myt',
		        id=c.person.url_hash, fragment=True))

                return render_response('registration/thankyou.myt')

        return render_response("registration/new.myt", defaults=defaults, errors=errors)

    def pay(self, id):
        registration = self.obj
        if registration.person.invoices:
            if registration.person.invoices[0].good_payments or registration.person.invoices[0].bad_payments:
                redirect_to("/Errors/InvoiceAlreadyPaid")
            invoice = registration.person.invoices[0]
            for ii in invoice.items:
                self.dbsession.delete(ii)
                
        else:
            invoice = model.Invoice()
            invoice.person = registration.person

        p = PaymentOptions()

        # Registration
        description = registration.type + " Registration"
        if p.is_earlybird(registration.creation_timestamp):
            description = description + " (earlybird)"
        cost = p.getTypeAmount(registration.type, registration.creation_timestamp)

        # Check for discount
        result, errors = self.check_discount()
        if result:
            discount = registration.discount
            description = description + " (Discounted " + discount.type + ")"
            discount_amount =  p.getTypeAmount(discount.type, registration.creation_timestamp) * discount.percentage/100
            if discount_amount > cost:
                cost = 0
            else:
                cost -= discount_amount

        ii = model.InvoiceItem(description=description, qty=1, cost=cost)
        self.dbsession.save(ii)
        invoice.items.append(ii)

        # Dinner:
        if registration.dinner > 0:
            iid = model.InvoiceItem(description='Additional Penguin Dinner Tickets',
                                    qty=registration.dinner,
                                    cost=p.getDinnerAmount(1))
            self.dbsession.save(iid)
            invoice.items.append(iid)
        
        # Accommodation:
        if registration.accommodation:
            description = 'Accommodation - %s' % registration.accommodation.name
            if registration.accommodation.option:
                description += " (%s)" % registration.accommodation.option
            iia = model.InvoiceItem(description,
                                    qty=registration.checkout-registration.checkin,
                                    cost=registration.accommodation.cost_per_night * 100)
            self.dbsession.save(iia)
            invoice.items.append(iia)

        # Partner's Programme
        partner = 0
        if registration.partner_email:
            iipa = model.InvoiceItem(description = "Partner's Programme - Adult",
                                     qty = 1,
                                     cost=20000)
            self.dbsession.save(iipa)
            invoice.items.append(iipa)
            
        kids = 0
        for k in [registration.kids_0_3, registration.kids_4_6, registration.kids_7_9, registration.kids_10]:
            if k is not None:
                kids += k
        if kids > 0:
            iipc = model.InvoiceItem(description="Partner's Programme - Child",
                                    qty = kids,
                                    cost=10000)
            self.dbsession.save(iipc)
            invoice.items.append(iipc)

        self.dbsession.save(invoice)
        self.dbsession.flush()

        redirect_to(controller='invoice', action='view', id=invoice.id)

    # FIXME There is probably a way to get this to use the List thingy from CRUD
    def remind(self):
        setattr(c, 'registration_collection', self.dbsession.query(self.model).select(order_by=self.model.c.id))
        return render_response('registration/remind.myt')

    def index(self):
        r = AuthRole('organiser')
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            if not r.authorise(self):
            	abort(403)
        else:
            abort(403)

	setattr(c, 'accommodation_collection', self.dbsession.query(Accommodation).select())


        return super(RegistrationController, self).index()

    def check_discount(self):
        registration = self.obj

        discount = registration.discount
        # No discount code match
        if not discount:
            return False, None

        if len(discount.registrations) > 1:
            return False, "Discount code already used"

        if discount.type != registration.type:
            error = "You're discount is for " + discount.type + ", but you are registering for " + registration.type + ". This is fine if what you are registering for is more expensive a bit silly otherwise."
            return True, error

        return True, "Your discount code has been applied"

    def status(self):
        return render_response("registration/status.myt")



class PaymentOptions:
    def __init__(self):
        self.types = {
                "Professional": [59840, 74800],
                "Hobbyist": [28160, 35200],
                "Concession": [15400, 15400],
                "Speaker": [0, 0]
                }
        self.dinner = 5000

# I think accomodation is in the DB?		
#        self.accommodation = {
#                "0": 0,
#                "1": 4950,
#                "2": 5500,
#                "3": 6000,
#                "5": 3500,
#                "6": 5850
#                }
        self.ebdate = datetime.datetime(2006, 11, 16, 00, 00, 00)
        #indates = [14, 15, 16, 17, 18, 19]
        #outdates = [15, 16, 17, 18, 19, 20]

    def getTypeAmount(self, type, date):
        if type in self.types.keys():
            if self.is_earlybird(date):
                return self.types[type][0]
            else:
                return self.types[type][1]

    def is_earlybird(self, date):
        result = date.date() < self.ebdate.date()
        return result

    def getDinnerAmount(self, tickets):
        dinnerAmount = self.dinner*tickets
        return dinnerAmount

#    def getAccommodationRate(self, choice):
#        accommodationRate = self.accommodation[choice]
#        return accommodationRate

#    def getAccommodationAmount(self, rate, indate, outdate):
#        accommodationAmount = (outdate - indate) * rate
#        return accommodationAmount

    def getPartnersAmount(self, partner, kids):
        count = partner + kids
        if count == 0:
            partnersAmount = 0
        else:
            partnersAmount = partner * 29700 + kids * 14300
        return partnersAmount



