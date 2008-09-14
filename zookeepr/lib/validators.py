import cgi
import re

import dns.resolver
from formencode import Invalid, validators, schema

import helpers as h

from zookeepr.model import Person, ProposalType, Stream, AssistanceType, DBContentType

class DictSet(validators.Set):
    def _from_python(self, value):
        value = super(DictSet, self)._from_python(value, state)
        return dict(zip(value, [1]*len(value)))

    def _to_python(self, value, state):
        value = value.keys()
        return super(DictSet, self)._to_python(value, state)

class BoundedInt(validators.Int):
    """ Validator for integers, with bounds.

    Just like validators.Int, but with optional max and min arguments that
    give limits on the integers and default to the PostgreSQL range for the
    integer type (-2147483648 to +2147483647).

    WTF did anyone ever code an Int validator *without* bounds?
    """

    def __init__(self, *args, **kw):
        validators.Int.__init__(self, *args, **kw)
        if not hasattr(self, 'min') or self.min==None:
            self.min = -2147483648 # Smallest number that fits in postgres
        if not hasattr(self, 'max') or self.max==None:
            self.max = +2147483647 # Largest number that fits in postgres
    def validate_python(self, value, state):
        if value>self.max:
            raise Invalid('Too large (maximum %d)'%self.max, value, state)
        if value<self.min:
            raise Invalid('Too small (minimum %d)'%self.min, value, state)

class BaseSchema(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    def validate(self, input, state=None):
        try:
            result = self.to_python(input, state)
            return result, {}
        except Invalid, e:
            errors = e.unpack_errors()
            # e.unpack_errors() doesn't necessarily return a nice dictionary
            # for formfill to use, so re-mangle it
            good_errors = {}
            try:
                for key in errors.keys():
                    try:
                        for subkey in errors[key].keys():
                            good_errors[key + "." + subkey] = errors[key][subkey]
                    except AttributeError:
                        good_errors[key] = errors[key]
            except AttributeError:
                good_errors['x'] = errors

            return {}, good_errors

#    def to_python(self, value_dict, state):
#        print value_dict
#        for key, value in value_dict.iteritems():
#            #if isinstance(value, str):
#                value_dict[key] = h.esc(value)
#        #print value_dict
#        return super(BaseSchema, self).to_python(value_dict, state)



class PersonValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Person.get(value)

class DbContentTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return state.query(DBContentType).get(value)

class ProposalTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return state.query(ProposalType).get(value)

class AssistanceTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return state.query(AssistanceType).get(value)

class FileUploadValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            filename = value.filename
            content = value.value
        elif isinstance(value, str):
            filename = None
            content = value
        if content.__len__() > 3000000: #This is not the right place to validate it, but at least it is validated...
            raise Invalid('Files must not be bigger than 2MB', value, state)
        return dict(filename=filename,
                    content=content)


class StreamValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return state.query(Stream).get(value)


class ReviewSchema(schema.Schema):
    score = BoundedInt()
    stream = StreamValidator()
    miniconf = validators.String()
    comment = validators.String()


class EmailAddress(validators.FancyValidator):
    """Validator for email addresses.

    We override the FormEncode Email validator because it doesn't
    allow domains that have A records but no MX, and doesn't like
    'localhost'.
    """

    usernameRE = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
    domainRE = re.compile(r"^[a-z0-9][a-z0-9\.\-_]*\.[a-z]+$|^localhost$", re.I)

    messages = {
        'empty': 'Please enter an email address',
        'noAt': 'An email address must contain a single @',
        'badUsername': 'The username portion of the email address is invalid (the portion before the @: %(username)s)',
        'badDomain': 'The domain portion of the email address is invalid (the portion after the @: %(domain)s)',
        'domainDoesNotExist': 'The domain of the email address does not exist (the portion after the @: %(domain)s)',
        'socketError': 'An error occurred when trying to connect to the server: %(error)s',
        'dnsTimeout': 'A temporary error occurred whilst trying to validate your email address, please try again in a moment.',
        }

    def __init__(self, *args, **kwargs):
        super(EmailAddress, self).__init__(*args, **kwargs)

    def validate_python(self, value, state):
        if not value:
            raise Invalid(self.message('empty', state), value, state)
        value = value.strip()
        splitted = value.split('@', 1)
        if not len(splitted) == 2:
            raise Invalid(self.message('noAt', state), value, state)
        if not self.usernameRE.search(splitted[0]):
            raise Invalid(self.message('badUsername', state, username=splitted[0]), value, state)
        if not self.domainRE.search(splitted[1]):
            raise Invalid(self.message('badDomain', state, domain=splitted[1]), value, state)

        # hack so example.org tests work offline
        domain_exists = False;
        if splitted[1] == 'example.org' or splitted[1] == 'localhost':
            domain_exists = True
        else:
            try:
                try:
                    domain_exists = dns.resolver.query(splitted[1], 'A')
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                    pass
                try:
                    domain_exists = dns.resolver.query(splitted[1], 'MX')
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                    pass
            except dns.resolver.Timeout:
                raise Invalid(self.message('dnsTimeout', state, domain=splitted[1]), value, state)
            if domain_exists == False:
                raise Invalid(self.message('domainDoesNotExist', state, domain=splitted[1]), value, state)

    def _to_python(self, value, state):
        return value.strip()

# TODO: have link to signin field
class NotExistingPersonValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        person = state.query(Person).filter_by(email_address=value['email_address']).first()
        if person is not None:
            raise Invalid("A person with this email already exists.  Please try signing in first.", value, state)

class ProductMinMax(validators.FancyValidator):
    def validate_python(self, value, state):
        total = 0
        for field in self.product_fields:
            try:
                total += int(value[field])
            except:
                pass
        if total < self.min_qty:
            raise Invalid("You must have at least " + str(self.min_qty) + ' ' + self.category_name, value, state)
        if total > self.max_qty:
            raise Invalid("You can not order more than " + str(self.max_qty) + ' ' + self.category_name, value, state)

class ProductInCategory(validators.FancyValidator):
    def validate_python(self, value, state):
        for product in self.category.products:
            if product.id == int(value) and product.available():
                return
        raise Invalid("Product " + value + " is not allowed in category " + self.category.name, value, state)

class PPEmail(validators.FancyValidator):
    # Check if a child in the PP has an adult with them
    # takes adult_field, email_field
    
    def validate_python(self, value, state):
        try:
            adult_field = int(value[self.adult_field])
        except:
            # no adult tickets = no tickets at all
            return
        if adult_field > 0 and value[self.email_field] == '':
            raise Invalid("You must supply a valid email address for the partners programme.", value, state)
        return

class PPChildrenAdult(validators.FancyValidator):
    # Check if a child in the PP has an adult with them
    # takes current_field, adult_field
    
    def validate_python(self, value, state):
        try:
            current_field = int(value[self.current_field])
        except:
            # they didn't order any of this field
            return
        try:
            adult_field = int(value[self.adult_field])
        except:
            raise Invalid("Any children in the partners programme must be accompanied by an adult.", value, state)

        # this if shouldn't actually be entered
        if current_field > 0 and adult_field < 1:
            raise Invalid("Any children in the partners programme must be accompanied by an adult.", value, state)
        return
