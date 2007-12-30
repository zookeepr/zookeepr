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
from zookeepr.model.billing import DiscountCode

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
        if value['type']=='Mini-conf organiser':
	    if 'signed_in_person_id' in session:
	        if not session['signed_in_person_id'] in PaymentOptions().miniconf_orgs:
		    raise Invalid("You don't appear to be a mini-conf organiser, don't claim a mini-conf organiser discount.", value, state)
	    else:
		raise Invalid("Please log in before claiming a mini-conf organiser discount!", value, state)
        if value['type']=='Team':
	    if 'signed_in_person_id' in session:
	        if 'team' not in [r.name for r in c.signed_in_person.roles]:
		    raise Invalid("You don't appear to be a team member, don't claim a team member discount.", value, state)
	    else:
		raise Invalid("Please log in before claiming a team member discount!", value, state)
        if value['type']=='Monday pass':
	    if 'signed_in_person_id' in session:
	        if 'monday-pass' not in [r.name for r in c.signed_in_person.roles]:
		    raise Invalid("You don't appear to be entitled to a Monday pass. ", value, state)
	    else:
		raise Invalid("Please log in before claiming a pass!", value, state)
        if value['type']=='Tuesday pass':
	    if 'signed_in_person_id' in session:
	        if 'tuesday-pass' not in [r.name for r in c.signed_in_person.roles]:
		    raise Invalid("You don't appear to be entitled to a Tuesday pass. ", value, state)
	    else:
		raise Invalid("Please log in before claiming a pass!", value, state)

class PPValidator(validators.FancyValidator):
    def validate_python(self, value, state):
	for k in ['kids_0_3', 'kids_4_6', 'kids_7_9', 'kids_10_11',
							     'kids_12_17']:
            if value[k] and not value['pp_adults']:
		raise Invalid("Can't have children without an adult in the partners programme", value, state)
	if value['partner_email'] and not value['pp_adults']:
	    raise Invalid("Please specify number of people in the partners programme (or remove partner's email address)", value, state)
	if value['pp_adults'] and not value['partner_email']:
	    raise Invalid("Please fill in partner's email address (or zero how many people are attending partners programme)", value, state)

class AccommodationValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if value == 'own':
            return None
        return state.query(model.Accommodation).get(value)

    def _from_python(self, value):
        return value.id

class NonblankForSpeakers(validators.String):
    def validate_python(self, value, state):
        validators.String.validate_python(self, value, state)
	if 'signed_in_person_id' in session:
            signed_in_person = state.query(model.Person).get_by(id=session['signed_in_person_id'])
	    is_speaker = reduce(lambda a, b: a or b.accepted,
					 signed_in_person.proposals, False)
	    if is_speaker and len(value)<3:
		raise Invalid("Missing value", value, state)

class TicketTypeValidator(validators.String):
    def validate_python(self, value, state):
        validators.String.validate_python(self, value, state)
	valid_tickets = ( "Fairy Penguin Sponsor", "Professional",
	    "Hobbyist", "Student", "Speaker", "Mini-conf organiser",
	    "Team", "Monday pass", "Tuesday pass", "Monday only",
	    "Tuesday only")
	if value not in valid_tickets:
	    raise Invalid("Invalid type", value, state)

class RegistrationSchema(Schema):
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    country = validators.String(not_empty=True)
    postcode = validators.String(not_empty=True)

    phone = NonblankForSpeakers()
    
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

    type = TicketTypeValidator(not_empty=True)
    discount_code = validators.String()

    teesize = validators.String(not_empty=True)
    extra_tee_count = BoundedInt(min=0)
    extra_tee_sizes = validators.String()
    dinner = BoundedInt(min=0)
    diet = validators.String()
    special = validators.String()
    miniconf = DictSet(if_missing=None)
    opendaydrag = BoundedInt(min=0)

    partner_email = EmailAddress(resolve_domain=True)
    kids_0_3 = BoundedInt(min=0)
    kids_4_6 = BoundedInt(min=0)
    kids_7_9 = BoundedInt(min=0)
    kids_10_11 = BoundedInt(min=0)
    kids_12_17 = BoundedInt(min=0)
    pp_adults = BoundedInt(min=0)
    speaker_pp_pay_adult = BoundedInt(min=0)
    speaker_pp_pay_child = BoundedInt(min=0)

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
	  SillyDescriptionMD5(), SpeakerDiscountValidator(), PPValidator()]

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


class RegistrationController(SecureController, Create, Update, List, Read):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               'edit': EditRegistrationSchema(),
               }
    redirect_map = {'edit': dict(controller='registration', action='status'),
                    }
    permissions = { 'remind': [AuthRole('organiser')],
		    'list_miniconf_orgs': [AuthRole('organiser')],
		    'professional': [AuthRole('organiser')],
		    'edit': [AuthFunc('is_same_person'), AuthRole('organiser')],
		    'view': [AuthFunc('is_same_person'), AuthRole('organiser')],
                   }
    anon_actions = ['status', 'new', 'index']

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

        c.accom_taken = self.accom_taken()
        as = self.dbsession.query(model.Accommodation).select()
	def space_available(a):
	  if is_speaker and a.name=='Trinity':
	    return True
	  return a.beds > c.accom_taken.get(a.name,0)
        c.accommodation_collection = filter(space_available, as)
	c.accommodation_collection.sort(cmp = lambda a, b: cmp(a.id, b.id))

    def edit(self, id):
        if not self.is_same_person() and not AuthRole('organiser').authorise(self):
            abort(403)

        registration = self.obj
        if registration.person.invoices:
            if registration.person.invoices[0].good_payments or registration.person.invoices[0].bad_payments:
	        c.invoice = registration.person.invoices[0]
                return render_response('invoice/already.myt')

	c.is_miniconf_org = c.signed_in_person and c.signed_in_person.id in PaymentOptions().miniconf_orgs
	try:
            return super(RegistrationController, self).edit(id)
	finally:
	    try:
	        self.pay(id, quiet=1) #regenerate the invoice
	    except:
	        self.pay(id, quiet=1) #retry once

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

		self.obj = c.registration
		self.pay(c.registration.id, quiet=1)

		if c.signed_in_person:
		    redirect_to('/registration/status')
                return render_response('registration/thankyou.myt')

	c.is_miniconf_org = c.signed_in_person and c.signed_in_person.id in PaymentOptions().miniconf_orgs
        return render_response("registration/new.myt", defaults=defaults, errors=errors)

    def pay(self, id, quiet=0):
        registration = self.obj
        if registration.person.invoices:
            if registration.person.invoices[0].good_payments or registration.person.invoices[0].bad_payments:
	        c.invoice = registration.person.invoices[0]
		if quiet: return
                return render_response('invoice/already.myt')
            invoice = registration.person.invoices[0]
            for ii in invoice.items:
                self.dbsession.delete(ii)
                
        else:
            invoice = model.Invoice()
            invoice.person = registration.person

        p = PaymentOptions()

	is_speaker = reduce(lambda a, b: a or b.accepted,
					 registration.person.proposals, False)

        # Check for discount
        discount_result, errors = self.check_discount()

	# Check conference ceiling
	rego_closed = not self.check_ceiling(registration.type).ok
	if discount_result:
	    rego_closed = False # discounted tickets are always available
	if is_speaker or registration.person.id in p.miniconf_orgs:
	    rego_closed = False # rego never closes for speakers or MC orgs

        # Registration
        description = registration.type + " Registration"
	eb = self.check_earlybird()[0]
        if eb and registration.type in ('Hobbyist', 'Professional'):
            description = description + " (earlybird)"
        if rego_closed:
            description = description + " (NOT AVAILABLE)"
        cost = p.getTypeAmount(registration.type, eb)

        ii = model.InvoiceItem(description=description, qty=1, cost=cost)
        self.dbsession.save(ii)
        invoice.items.append(ii)

        if discount_result:
            discount = registration.discount
            description = discount.comment
            discount_amount =  p.getTypeAmount(discount.type, eb) * discount.percentage/100.0
            if discount_amount > cost:
                discount_amount = cost

	    ii = model.InvoiceItem(description=description, qty=1,
						     cost=-discount_amount)
	    self.dbsession.save(ii)
	    invoice.items.append(ii)

        if rego_closed:
            iia = model.InvoiceItem('INVALID INVOICE (registration closed)',
                                    qty=1,
                                    cost=1)
            self.dbsession.save(iia)
            invoice.items.append(iia)

        # extra T-shirts:
        if registration.extra_tee_count > 0:
            iid = model.InvoiceItem(description='Additional T-shirts',
                                    qty=registration.extra_tee_count,
                                    cost=2475)
            self.dbsession.save(iid)
            invoice.items.append(iid)
        
        # Dinner:
        if registration.dinner > 0:
            iid = model.InvoiceItem(description='Additional Penguin Dinner Tickets',
                                    qty=registration.dinner,
                                    cost=p.getDinnerAmount(1))
            self.dbsession.save(iid)
            invoice.items.append(iid)
        
        # Accommodation:
	accom_not_available = False
        if registration.accommodation:
            description = 'Accommodation - %s' % registration.accommodation.name
            if registration.accommodation.option:
                description += " (%s)" % registration.accommodation.option
            accom_qty=registration.checkout-registration.checkin
	    while accom_qty<0: accom_qty += 31 #January has 31 days
            accom_cost=registration.accommodation.cost_per_night * 100
	    if registration.accommodation.beds <= \
		     c.accom_taken.get(registration.accommodation.name, 0):
                if registration.accommodation.name=='Trinity' and \
                   registration.accommodation.option=='speaker':
		     pass
                else:
		   description += " (NOT AVAILABLE)"
                   #accom_cost += 1
		   accom_not_available = True
		   
            iia = model.InvoiceItem(description,
                                    qty=accom_qty,
                                    cost=accom_cost)
            self.dbsession.save(iia)
            invoice.items.append(iia)

        if accom_not_available:
            iia = model.InvoiceItem('INVALID INVOICE (accommodation full)',
                                    qty=1,
                                    cost=1)
            self.dbsession.save(iia)
            invoice.items.append(iia)

        # Partner's Programme
        if is_speaker:
	  partner = registration.speaker_pp_pay_adult
        else:
	  partner = 0
	  for p in [registration.kids_12_17, registration.pp_adults]:
	    if p is not None:
	      partner += p
        if partner > 0:
            iipa = model.InvoiceItem(description = "Partner's Programme - Adult",
                                     qty = partner,
                                     cost=22000)
            self.dbsession.save(iipa)
            invoice.items.append(iipa)
            
        if is_speaker:
	  kids = registration.speaker_pp_pay_child
        else:
	  kids = 0
	  for k in [registration.kids_0_3, registration.kids_4_6, registration.kids_7_9, registration.kids_10_11]:
	      if k is not None:
		  kids += k
        if kids > 0:
            iipc = model.InvoiceItem(description="Partner's Programme - Child",
                                    qty = kids,
                                    cost=13200)
            self.dbsession.save(iipc)
            invoice.items.append(iipc)

	invoice.last_modification_timestamp = 'now'
	invoice.due_date = 'now'

        self.dbsession.save(invoice)
        self.dbsession.flush()

	if quiet: return
	if rego_closed:
            return render_response('registration/rego_closed.myt')
	if accom_not_available:
            return render_response('registration/accom_full.myt')
        redirect_to(controller='invoice', action='view', id=invoice.id)

    def list_miniconf_orgs(self):
        c.data = []
        for mc_id in PaymentOptions().miniconf_orgs:
	    row = ['<a href="/profile/%d">%d</a>' % (mc_id, mc_id)]
            mc = self.dbsession.query(model.Person).get_by(id=mc_id)
	    if mc==None:
		row.append('(unknown)')
	    else:
		row += (mc.firstname, mc.lastname, mc.email_address)
		if mc.registration is None:
		    row.append('(no rego)')
		else:
		    r = mc.registration
		    row += ('<a href="/registration/%d">%d</a>'%(r.id, r.id),
								    r.type)
		    if not mc.invoice:
			row += ('no invoice',)
		    elif mc.is_speaker():
			row += ('speaker',)
		    elif mc.invoice[0].paid():
			row += ('<a href="/invoice/%d">paid</a>' %
							 mc.invoice[0].id,)
		    else:
			row += ('<a href="/invoice/%d">owes $%.2f</a>' %
			 (mc.invoice[0].id, mc.invoice[0].total()/100.0), )
	    c.data.append(row)
	c.noescape=True
	return render_response('admin/table.myt')

    def accom_taken(self):
        res = {}
        for r in self.dbsession.query(model.Registration).select():
	    if r.accommodation==None: continue
	    paid = r.person.invoices and r.person.invoices[0].paid()
	    if r.accommodation.option != 'speaker':
		if not paid and not r.person.is_speaker():
		    continue
	    location = r.accommodation.name
	    if (r.accommodation.name=='Trinity' and
		r.accommodation.option=='speaker'):
		    location = 'Trinity-speaker'
	    res[location] = res.get(location, 0)+1
        return res

    # FIXME There is probably a way to get this to use the List thingy from CRUD
    def remind(self):
        setattr(c, 'registration_collection', self.dbsession.query(self.model).select(order_by=self.model.c.id))
        return render_response('registration/remind.myt')

    def index(self):
        r = AuthRole('organiser')
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            if not r.authorise(self):
		redirect_to('/registration/status')
        else:
	    redirect_to('/registration/status')

	setattr(c, 'accommodation_collection', self.dbsession.query(Accommodation).select())
	setattr(c, 'ebdate', PaymentOptions().ebdate)

        (c.eb, c.ebtext) = self.check_earlybird()
	c.ceiling = self.check_ceiling()

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
            error = "Your discount is for " + discount.type + ", but you are registering for " + registration.type + ". This is fine if what you are registering for is more expensive, a bit of a waste otherwise."
            return True, error

        return True, "Your discount code has been applied"

    def check_earlybird(self):
        count = 0
	po = PaymentOptions()
	timeleft = po.ebdate - datetime.datetime.now()
	if timeleft < datetime.timedelta(0):
	    return False, "Too late."
	timeleft = " %.1f days to go." % (timeleft.days +
					     timeleft.seconds / (3600*24.))
        for r in self.dbsession.query(self.model).select():
	    if r.type not in ('Hobbyist', 'Professional'):
	        continue
	    if not r.person.invoices or not r.person.invoices[0].paid():
	        continue
	    if r.discount_code and r.discount_code.startswith('GOOGLE-'):
	        continue
		# see below about GOOGLE
	    speaker = 0
	    if r.person.proposals:
		for proposal in r.person.proposals:
		    if proposal.accepted:
			speaker = 1
	    if not speaker:
	        count += 1
	count += 20 # GOOGLE group booking is deemed all earlybird
	count += 10 # other group bookings
	if count >= po.eblimit:
	    return False, "All gone."
	left = po.eblimit - count
	percent = int(round((20.0 * left) / po.eblimit) * 5)
	if percent == 0:
	    return True, ("Almost all earlybirds gone," + timeleft)
	elif percent <= 30:
	    return True, ("Only %d%% earlybirds left,"%percent + timeleft)
	else:
	    return True, ("%d%% earlybirds left,"%percent + timeleft)

    def check_ceiling(self, check_type=None):
	""" Checks the ceiling, returning various information in a struct.
	Given a registration type, it also returns whether it's OK to
	register for that type (returned in the .ok field). """

        class struct: pass
	res = struct()
        res.regos = 0; res.disc_regos = 0
	ceiling_types = ('Student', 'Concession', 'Hobbyist',
				   'Professional', 'Fairy Penguin Sponsor')
        for r in self.dbsession.query(self.model).select():
	    if r.type not in ceiling_types:
	        continue
	    if not r.person.invoices or not r.person.invoices[0].paid():
	        continue
	    if r.discount_code and r.discount_code!='':
	        res.disc_regos += 1
	    res.regos += 1
	res.discounts = len(self.dbsession.query(DiscountCode).select())
	res.total = res.regos + res.discounts - res.disc_regos
	res.limit = 505
	res.open = res.total < res.limit

	if res.open:
	  res.left = res.limit - res.total
	  percent = int(round((20.0 * res.left) / res.limit) * 5)
	  if percent == 0:
	      res.text = "Almost all tickets gone."
	  elif percent <= 30:
	      res.text = "Only %d%% tickets left."%percent
	  else:
	      res.text = "%d%% tickets left."%percent
	else:
	    res.text = 'All tickets gone.'

        if check_type:
	    if check_type in ceiling_types:
	        res.ok = res.open
	    else:
	        res.ok = True

	return res

    def status(self):
        (c.eb, c.ebtext) = self.check_earlybird()
	c.ceiling = self.check_ceiling()
        return render_response("registration/status.myt")

    def professional(self):
        c.fairies = []; c.profs = []
        for r in self.dbsession.query(self.model).select():
            p = r.person; i = p.invoices
            if (i and i[0].paid()) or p.is_speaker():
		if r.type=='Fairy Penguin Sponsor':
		    c.fairies.append((p, r))
		elif r.type=='Professional':
		    c.profs.append((p, r))

        def name_cmp(a, b):
            return (cmp(a[0].lastname.lower(), b[0].lastname.lower()) or
		       cmp(a[0].firstname.lower(), b[0].firstname.lower()))
        def company_cmp(a, b):
            return (cmp(a[1].company.lower(), b[1].company.lower()) or
		       cmp(a[0].lastname.lower(), b[0].lastname.lower()) or
		       cmp(a[0].firstname.lower(), b[0].firstname.lower()))

        c.profs += c.fairies

        c.fairies.sort(company_cmp)
        c.profs.sort(name_cmp)

        return render_response('registration/professional.myt')

class PaymentOptions:
    def __init__(self):
        self.types = {
                "Fairy Penguin Sponsor": [165000, 165000],
                "Professional": [59840, 74800],
                "Hobbyist": [28160, 35200],
                "Concession": [15400, 15400],
                "Student": [15400, 15400],
                "Speaker": [0, 0],
                "Mini-conf organiser": [0, 0],
                "Team": [0, 0],
                "Monday pass": [0, 0],
                "Tuesday pass": [0, 0],
                "Monday only": [4950, 4950],
                "Tuesday only": [4950, 4950],
                }
        self.dinner = 5000
	self.miniconf_orgs = [35, 123, 15, 36, 55, 29, 18, 22, 86, 66, 46,
	        73, 71, 496, 81, 44, 279, 50014, 50283,
		]

# I think accomodation is in the DB?		
#        self.accommodation = {
#                "0": 0,
#                "1": 4950,
#                "2": 5500,
#                "3": 6000,
#                "5": 3500,
#                "6": 5850
#                }
        self.ebdate = datetime.datetime(2007, 11, 18, 00, 00, 00)
        self.eblimit = 220
        #indates = [14, 15, 16, 17, 18, 19]
        #outdates = [15, 16, 17, 18, 19, 20]

    def getTypeAmount(self, type, eb):
        if type in self.types.keys():
            if eb:
                return self.types[type][0]
            else:
                return self.types[type][1]

#    def is_earlybird(self, date):
#        result = date.date() < self.ebdate.date()
#        return result

    def getDinnerAmount(self, tickets):
        dinnerAmount = self.dinner*tickets
        return dinnerAmount

#    def getAccommodationRate(self, choice):
#        accommodationRate = self.accommodation[choice]
#        return accommodationRate

#    def getAccommodationAmount(self, rate, indate, outdate):
#        accommodationAmount = (outdate - indate) * rate
#        return accommodationAmount

#    def getPartnersAmount(self, partner, kids):
#        count = partner + kids
#        if count == 0:
#            partnersAmount = 0
#        else:
#            partnersAmount = partner * 22000 + kids * 13200
#        return partnersAmount



