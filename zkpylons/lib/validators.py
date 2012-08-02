import formencode
from formencode import validators, Invalid #, schema

from zkpylons.model import Person, Proposal, ProposalType, TargetAudience
from zkpylons.model import ProposalStatus, Stream, AccommodationAssistanceType
from zkpylons.model import TravelAssistanceType, DbContentType, Registration
from zkpylons.model import Product, ProductCategory, Ceiling, FundingType
from zkpylons.model import FundingStatus, Funding
from zkpylons.model import Invoice, Payment
from zkpylons.model import SocialNetwork

from zkpylons.config.lca_info import lca_info

import cgi

def check_product_availability(product, value, state):
    if product.available():
        return
    elif product.available(stock=False):
        raise Invalid(product.description + " has unfortunately sold out.", value, state)
    else:
        raise Invalid(product.description + " is not available.", value, state)

class BaseSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

class DictSet(validators.Set):
    def _from_python(self, value, state):
        value = super(DictSet, self)._from_python(value, state)
        return dict(zip(value, [1]*len(value)))

    def _to_python(self, value, state):
        value = value.keys()
        return super(DictSet, self)._to_python(value, state)

class IAgreeValidator(validators.FormValidator):
    validate_partial_form = True
    def __init__(self, field_name):
        super(self.__class__, self).__init__()
        self.__field_name = field_name
    def validate_partial(self, values, state):
        agree_value = values.get(self.__field_name, None)
        if not agree_value:
            error_dict = {
                self.__field_name: "You must read and accept the terms and conditions before you can register.",
            }
            raise Invalid(self.__class__.__name__, values, state, error_dict=error_dict)

class PersonValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Person.find_by_id(int(value))

class CountryValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        from zkpylons.lib.helpers import countries
        if value not in countries():
            raise Invalid('Not a valid country', value, state)
        return value

class DbContentTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return DbContentType.find_by_id(value)

class ProposalValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Proposal.find_by_id(int(value))

class ProposalTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return ProposalType.find_by_id(value)

class TargetAudienceValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return TargetAudience.find_by_id(value)

class AccommodationAssistanceTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return AccommodationAssistanceType.find_by_id(value)

class TravelAssistanceTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return TravelAssistanceType.find_by_id(value)

class ProposalStatusValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return ProposalStatus.find_by_id(int(value))

class FileUploadValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            filename = value.filename
            content = value.value
        elif isinstance(value, unicode) or isinstance(value, str):
            filename = None
            content = value
        if len(content) > 3000000: #This is not the right place to validate it, but at least it is validated...
            raise Invalid('Files must not be bigger than 2MB', value, state)
        return dict(filename=filename, content=content)

class FundingTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        funding_type = FundingType.find_by_id(int(value))
        if funding_type != None and funding_type.available():
          return funding_type
        else:
          return False

class FundingStatusValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return FundingStatus.find_by_id(int(value))

class FundingValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Funding.find_by_id(int(value))

class StreamValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if value in ("", "None", None):
            return None
        else:
            return Stream.find_by_id(value)

    def _from_python(self, value, state):
        return value.id

class ProductValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Product.find_by_id(value)

    def _from_python(self, value, state):
        return value.id

class CeilingValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Ceiling.find_by_id(value)

    def _from_python(self, value, state):
        return value.id

class SocialNetworkValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return SocialNetwork.find_by_id(value)

    def _from_python(self, value, state):
        return value.id

class ProductCategoryValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return ProductCategory.find_by_id(value)

    def _from_python(self, value, state):
        return value.id

class ReviewSchema(BaseSchema):
    score = validators.OneOf(["-2", "-1", "1", "2"], if_missing=None)
    stream = StreamValidator()
    miniconf = validators.String()
    comment = validators.String()
    private_comment = validators.String()

class FundingReviewSchema(BaseSchema):
    score = validators.OneOf(["-2", "-1", "+1", "+2", "null"])
    comment = validators.String()

class ExistingRegistrationValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        registration = Registration.find_by_id(int(value), abort_404=False)
        if registration is None:
            raise Invalid("Unknown registration ID.", value, state)
        else:
            return registration
    def _from_python(self, value, state):
        return value.id

class ExistingInvoiceValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        invoice = Invoice.find_by_id(int(value), False)
        if invoice is None:
            raise Invalid("Unknown invoice ID.", value, state)
        else:
            return invoice
    def _from_python(self, value, state):
        return value.id

class ExistingPaymentValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        payment = Payment.find_by_id(int(value), abort_404=False)
        if payment is None:
            raise Payment("Unknown payment ID.", value, state)
        else:
            return payment
    def _from_python(self, value, state):
        return value.id

class ExistingPersonValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        person = Person.find_by_id(int(value), abort_404=False)
        if person is None:
            raise Invalid("Unknown person ID.", value, state)
        else:
            return person
    def _from_python(self, value, state):
        return value.id

class ExistingPersonValidator_by_email(validators.FancyValidator):
    def validate_python(self, value, state):
        person = Person.find_by_email(value)
        if person is None:
            msg = 'Your supplied e-mail does not exist in our database. Please try again or if you continue to have problems, contact %s.' % lca_info['contact_email']
            raise Invalid(msg, value, state, error_dict={'email_address': msg})

class NotExistingPersonValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        person = Person.find_by_email(values['email_address'])
        if person is not None:
            msg = "A person with this email already exists. Please try signing in first."
            raise Invalid(msg, values, state, error_dict={'email_address': msg})

class SameEmailAddress(validators.FancyValidator):
    def validate_python(self, values, state):
        if values['email_address'] != values['email_address2']:
            msg = 'Email addresses don\'t match'
            raise Invalid(msg, values, state, error_dict={'email_address2': msg})

class PersonSchema(BaseSchema):
    #allow_extra_fields = False

    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    company = validators.String()
    email_address = validators.Email(not_empty=True)
    email_address2 = validators.Email(not_empty=True)
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
    i_agree = validators.Bool(if_missing=False)

    chained_validators = [NotExistingPersonValidator(), validators.FieldsMatch('password', 'password_confirm'), SameEmailAddress(), IAgreeValidator("i_agree")]


class ProductMinMax(validators.FancyValidator):
    """ Check the Category min/max requirements are met.
        self.product_fields is a [list] of products (generally category.products)
        self.min_qty is the minimum total (generally category.min)
        self.max_qty is the maximum total (generally category.max)

        See zkpylons.registration.RegistrationController._generate_product_schema for examples
    """
    def validate_python(self, values, state):
        total = 0
        error_dict = {}
        for field in self.product_fields:
            try:
                value = values.get(field, None)
                if value is None:
                    pass
                elif value < 0:
                    error_dict[field] = "Must be positive."
                else:
                    total += value
            except:
                pass
        if total < self.min_qty:
            error_dict[self.error_field_name] = "You must have at least %d %s" % (self.min_qty, self.category_name,)
        if total > self.max_qty:
            error_dict[self.error_field_name] = "You can not order more than %d %s" % (self.max_qty, self.category_name,)
        if error_dict:
            error_message = "Quantities for %s are incorrect" % self.category_name
            raise Invalid(error_message, values, state, error_dict=error_dict)

class ProductInCategory(validators.FancyValidator):
    """ Check to see if product is available """
    def validate_python(self, value, state):
        p = Product.find_by_id(int(value))
        for product in Product.find_by_category(p.category.id):
            if product.id == int(value):
                check_product_availability(product, value, state)
                return # All good!
        raise Invalid("Product " + value + " is not allowed in category " + self.category.name, value, state)

class ProductQty(validators.Int):
    def __init__(self, *args, **kw):
        validators.Int.__init__(self, *args, **kw)
        if not hasattr(self, 'min') or self.min==None:
            self.min = 0
        if not hasattr(self, 'max') or self.max==None:
            self.max = +2147483647 # Largest number that fits in postgres

    def validate_python(self, value, state):
        if value>self.max:
            raise Invalid('Too large (maximum %d)'%self.max, value, state)
        if value<self.min:
            raise Invalid('Too small (minimum %d)'%self.min, value, state)
        if int(value) != 0:
            check_product_availability(self.product, value, state)

class CheckboxQty(validators.Bool):
    def validate_python(self, value, state):
        if value:
            check_product_availability(self.product, value, state)

class PPDetails(validators.FancyValidator):
    # Check if a child in the PP has an adult with them
    # takes adult_field, email_field

    def validate_python(self, values, state):
        error_dict = {}
        try:
            adult_field = int(values[self.adult_field])
        except:
            # no adult tickets = no tickets at all
            return
        if adult_field > 0 and values[self.email_field] == '':
            error_dict[self.email_field] = "You must supply a valid email address for the partners programme."
        if adult_field > 0 and values[self.name_field] == '':
            error_dict[self.name_field] = "You must supply a valid name for the partners programme."
        if adult_field > 0 and values[self.mobile_field] == '':
            error_dict[self.mobile_field] = "You must supply a valid mobile number for the partners programme."
        if error_dict:
            raise Invalid("Partners Program details are incorrect", values, state, error_dict=error_dict)

class ProDinner(validators.FancyValidator):
    # If they select a professional ticket, force the dinner ticket
    # takes dinner_field, ticket_category and ticket_id list

    def validate_python(self, values, state):
        try:
            ticket = int(values[self.ticket_category])
        except:
            # they haven't gotten a ticket yet
            return
        if not self.dinner_field in values:
            # the Speakers Dinner field is not present for non-speakers
            return
        error_dict = {}
        if values[self.dinner_field] is None and ticket in self.ticket_id:
            error_dict[self.error_field_name] = "The ticket you have chosen includes one free dinner ticket. If you do not wish to attend the dinner please enter 0 into the field. Otherwise enter the number of tickets you would like, including yourself."
        if error_dict:
            raise Invalid("Dinners are incorrect", values, state, error_dict=error_dict)

class PPChildrenAdult(validators.FancyValidator):
    # Check if a child in the PP has an adult with them
    # takes current_field, adult_field

    def validate_python(self, values, state):
        try:
            current_field = int(values[self.current_field])
        except:
            # they didn't order any of this field
            return
        error_dict = {}
        try:
            adult_field = int(values[self.adult_field])
        except:
            error_dict[self.adult_field] = "Any children in the partners programme must be accompanied by an adult."
        else:
            if current_field > 0 and adult_field < 1:
                error_dict[self.adult_field] = "Any children in the partners programme must be accompanied by an adult."
        if error_dict:
            raise Invalid("Dinners are incorrect", values, state, error_dict=error_dict)
