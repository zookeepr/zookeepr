import formencode
from formencode import validators, Invalid #, schema

from zookeepr.model import Person, AssistanceType, ProposalType, Stream, DbContentType

from zookeepr.config.lca_info import lca_info

import cgi


class BaseSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

#import re
#
#import dns.resolver
#from formencode import Invalid, validators, schema
#
#import helpers as h
#
#from zookeepr.model import Person, ProposalType, Stream, AssistanceType, DBContentType, Product, Registration
#
#class DictSet(validators.Set):
#    def _from_python(self, value):
#        value = super(DictSet, self)._from_python(value, state)
#        return dict(zip(value, [1]*len(value)))
#
#    def _to_python(self, value, state):
#        value = value.keys()
#        return super(DictSet, self)._to_python(value, state)
#
#class BoundedInt(validators.Int):
#    """ Validator for integers, with bounds.
#
#    Just like validators.Int, but with optional max and min arguments that
#    give limits on the integers and default to the PostgreSQL range for the
#    integer type (-2147483648 to +2147483647).
#
#    WTF did anyone ever code an Int validator *without* bounds?
#    """
#
#    def __init__(self, *args, **kw):
#        validators.Int.__init__(self, *args, **kw)
#        if not hasattr(self, 'min') or self.min==None:
#            self.min = -2147483648 # Smallest number that fits in postgres
#        if not hasattr(self, 'max') or self.max==None:
#            self.max = +2147483647 # Largest number that fits in postgres
#    def validate_python(self, value, state):
#        if value>self.max:
#            raise Invalid('Too large (maximum %d)'%self.max, value, state)
#        if value<self.min:
#            raise Invalid('Too small (minimum %d)'%self.min, value, state)
#

#
#class PersonValidator(validators.FancyValidator):
#    def _to_python(self, value, state):
#        return Person.get(value)
#

class DbContentTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return DbContentType.find_by_id(value)

class ProposalTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return ProposalType.find_by_id(value)

class AssistanceTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return AssistanceType.find_by_id(value)

class FileUploadValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            filename = value.filename
            content = value.value
        elif isinstance(value, str):
            filename = None
            content = value
        if len(content) > 3000000: #This is not the right place to validate it, but at least it is validated...
            raise Invalid('Files must not be bigger than 2MB', value, state)
        return dict(filename=filename, content=content)


class StreamValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Stream.find_by_id(value)

#class ProductValidator(validators.FancyValidator):
#    def _to_python(self, value, state):
#        return state.query(Product).get(value)
#
#    def _from_python(self, value, state):
#        return value.id

class ReviewSchema(BaseSchema):
    score = validators.OneOf(["-2", "-1", "+1", "+2"])
    stream = StreamValidator()
    miniconf = validators.String()
    comment = validators.String()


#class EmailAddress(validators.FancyValidator):
#    """Validator for email addresses.
#
#    We override the FormEncode Email validator because it doesn't
#    allow domains that have A records but no MX, and doesn't like
#    'localhost'.
#    """
#
#    usernameRE = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
#    domainRE = re.compile(r"^[a-z0-9][a-z0-9\.\-_]*\.[a-z]+$|^localhost$", re.I)
#
#    messages = {
#        'empty': 'Please enter an email address',
#        'noAt': 'An email address must contain a single @',
#        'badUsername': 'The username portion of the email address is invalid (the portion before the @: %(username)s)',
#        'badDomain': 'The domain portion of the email address is invalid (the portion after the @: %(domain)s)',
#        'domainDoesNotExist': 'The domain of the email address does not exist (the portion after the @: %(domain)s)',
#        'socketError': 'An error occurred when trying to connect to the server: %(error)s',
#        'dnsTimeout': 'A temporary error occurred whilst trying to validate your email address, please try again in a moment.',
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(EmailAddress, self).__init__(*args, **kwargs)
#
#    def validate_python(self, value, state):
#        if not value:
#            raise Invalid(self.message('empty', state), value, state)
#        value = value.strip()
#        splitted = value.split('@', 1)
#        if not len(splitted) == 2:
#            raise Invalid(self.message('noAt', state), value, state)
#        if not self.usernameRE.search(splitted[0]):
#            raise Invalid(self.message('badUsername', state, username=splitted[0]), value, state)
#        if not self.domainRE.search(splitted[1]):
#            raise Invalid(self.message('badDomain', state, domain=splitted[1]), value, state)
#
#        # hack so example.org tests work offline
#        domain_exists = False;
#        if splitted[1] == 'example.org' or splitted[1] == 'localhost':
#            domain_exists = True
#        else:
#            try:
#                try:
#                    domain_exists = dns.resolver.query(splitted[1], 'A')
#                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
#                    pass
#                try:
#                    domain_exists = dns.resolver.query(splitted[1], 'MX')
#                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
#                    pass
#            except dns.resolver.Timeout:
#                raise Invalid(self.message('dnsTimeout', state, domain=splitted[1]), value, state)
#            if domain_exists == False:
#                raise Invalid(self.message('domainDoesNotExist', state, domain=splitted[1]), value, state)
#
#    def _to_python(self, value, state):
#        return value.strip()
#
#class ExistingRegistrationValidator(validators.FancyValidator):
#    def _to_python(self, value, state):
#        registration = state.query(Registration).filter_by(id=value).first()
#        if registration is None:
#            raise Invalid("Unknown registration ID.", value, state)
#        else:
#            return registration
#    def _from_python(self, value, state):
#        return value.id
#

class ExistingPersonValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        print value
        person = Person.find_by_email(value['email_address'])
        if person is None:
            msg = 'Your supplied e-mail does not exist in our database. Please try again or if you continue to have problems, contact %s.' % lca_info['contact_email']
            raise Invalid(msg, value, state, error_dict={'email_address': msg})

class NotExistingPersonValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        person = Person.find_by_email(value['email_address'])
        if person is not None:
            msg = "A person with this email already exists. Please try signing in first."
            raise Invalid(msg, value, state, error_dict={'email_address': msg})

class PersonSchema(BaseSchema):
    allow_extra_fields = False

    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    company = validators.String()
    email_address = validators.Email(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True)
    country = validators.String(not_empty=True)

    chained_validators = [NotExistingPersonValidator(), validators.FieldsMatch('password', 'password_confirm')]



#class ProductMinMax(validators.FancyValidator):
#    def validate_python(self, value, state):
#        total = 0
#        negative_products = False
#        for field in self.product_fields:
#            try:
#                if int(value[field]) < 0:
#                    negative_products = True
#                else:
#                    total += int(value[field])
#            except:
#                pass
#        if negative_products:
#            raise Invalid("You can not have negative products. Please correct your " + self.category_name, value, state)
#        if total < self.min_qty:
#            raise Invalid("You must have at least " + str(self.min_qty) + ' ' + self.category_name, value, state)
#        if total > self.max_qty:
#            raise Invalid("You can not order more than " + str(self.max_qty) + ' ' + self.category_name, value, state)
#
#class CheckAccomDates(validators.FancyValidator):
#    def __init__(self, *args, **kw):
#        validators.FancyValidator.__init__(self, *args, **kw)
#        if not hasattr(self, 'checkin') or self.checkin==None:
#            self.checkin = 'checkin' # Smallest number that fits in postgres
#        if not hasattr(self, 'checkout') or self.checkout==None:
#            self.checkout = 'checkout' # Largest number that fits in postgres
#
#    def validate_python(self, value, state):
#        if value[self.checkin] >= value[self.checkout]:
#            raise Invalid("Your checkin date must be before your check out.", value, state)
#        return
#
#class ProductInCategory(validators.FancyValidator):
#    def validate_python(self, value, state):
#        for product in self.category.products:
#            if product.id == int(value) and product.available():
#                return
#            elif product.id == int(value) and product.available(stock=False):
#                raise Invalid("The selected product, " + product.description + ", has unfortunately sold out.", value, state)
#        raise Invalid("Product " + value + " is not allowed in category " + self.category.name, value, state)
#
#class ProductCheckbox(validators.FancyValidator):
#    def validate_python(self, value, state):
#        if int(value) == 1 and not self.product.available():
#            raise Invalid("The selected product, " + self.product.description + ", has unfortunately sold out.", value, state)
#        return
#
#class ProductQty(validators.Int):
#    def __init__(self, *args, **kw):
#        validators.Int.__init__(self, *args, **kw)
#        if not hasattr(self, 'min') or self.min==None:
#            self.min = 0
#        if not hasattr(self, 'max') or self.max==None:
#            self.max = +2147483647 # Largest number that fits in postgres
#
#    def validate_python(self, value, state):
#        if value>self.max:
#            raise Invalid('Too large (maximum %d)'%self.max, value, state)
#        if value<self.min:
#            raise Invalid('Too small (minimum %d)'%self.min, value, state)
#        if not self.product.available() and int(value) != 0:
#            raise Invalid("The selected product, " + self.product.description + ", has unfortunately sold out.", value, state)
#        return
#
#class PPEmail(validators.FancyValidator):
#    # Check if a child in the PP has an adult with them
#    # takes adult_field, email_field
#
#    def validate_python(self, value, state):
#        try:
#            adult_field = int(value[self.adult_field])
#        except:
#            # no adult tickets = no tickets at all
#            return
#        if adult_field > 0 and value[self.email_field] == '':
#            raise Invalid("You must supply a valid email address for the partners programme.", value, state)
#        return
#
#class ProDinner(validators.FancyValidator):
#    # If they select a professional ticket, force the dinner ticket
#    # takes dinner_field, ticket_category and ticket_id list
#
#    def validate_python(self, value, state):
#        try:
#            ticket = int(value[self.ticket_category])
#        except:
#            #they haven't gotten a ticket yet
#            return
#        if len(value[self.dinner_field]) == 0 and ticket in self.ticket_id:
#            raise Invalid("The ticket you have chosen includes one free dinner ticket, however you haven't enterered anything into the Dinner tickets box. If you do not wish to attend the dinner please enter 0 into the field. Otherwise enter the number of tickets you would like, including yourself.", value, state)
#        return
#
#class PPChildrenAdult(validators.FancyValidator):
#    # Check if a child in the PP has an adult with them
#    # takes current_field, adult_field
#
#    def validate_python(self, value, state):
#        try:
#            current_field = int(value[self.current_field])
#        except:
#            # they didn't order any of this field
#            return
#        try:
#            adult_field = int(value[self.adult_field])
#        except:
#            raise Invalid("Any children in the partners programme must be accompanied by an adult.", value, state)
#
#        # this if shouldn't actually be entered
#        if current_field > 0 and adult_field < 1:
#            raise Invalid("Any children in the partners programme must be accompanied by an adult.", value, state)
#        return
