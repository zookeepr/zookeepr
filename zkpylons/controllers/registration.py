# coding=utf-8
import logging
import re

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.controllers.util import Response
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, DictSet, ProductInCategory, CheckboxQty
from zkpylons.lib.validators import ProductQty, ProductMinMax, IAgreeValidator, CountryValidator

# validators used from the database
from zkpylons.lib.validators import ProDinner, PPDetails, PPChildrenAdult

import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Registration, Role, RegistrationProduct, Person
from zkpylons.model import ProductCategory, Product, Voucher, Ceiling
from zkpylons.model import Invoice, InvoiceItem
from zkpylons.model.special_offer import SpecialOffer
from zkpylons.model.special_registration import SpecialRegistration
from zkpylons.model.config import Config

from zkpylons.controllers.person import PersonSchema

log = logging.getLogger(__name__)

import datetime

class CheckAccomDates(validators.FormValidator):
    def __init__(self, checkin_name, checkout_name):
        super(self.__class__, self).__init__()
        self.checkin = checkin_name
        self.checkout = checkout_name
    def validate_python(self, values, state):
        if values[self.checkin] >= values[self.checkout]:
            error_dict = {
                self.checkin:       "Your checkin date must be before your check out",
                self.checkout:      "Your checkout date must be after your check in.",
            }
            raise Invalid(self.__class__.__name__, values, state, error_dict=error_dict)

class VoucherValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        voucher = Voucher.find_by_code(value)
        if voucher != None:
            if voucher.registration:
                if voucher.registration.person.id != h.signed_in_person().id:
                    raise Invalid("Voucher code already in use!", value, state)
        elif value:
            raise Invalid("Unknown voucher code!", value, state)

class SillyDescriptionChecksum(validators.FormValidator):
    def __init__(self, silly_name, checksum_name):
        super(self.__class__, self).__init__()
        self.__silly_name = silly_name
        self.__checksum_name = checksum_name
    def validate_python(self, values, state):
        silly_description = values.get(self.__silly_name, None)
        if silly_description is None:
            return
        checksum = h.silly_description_checksum(silly_description)
        if values.get(self.__checksum_name, None) != checksum:
            error_dict = {
                self.__silly_name: "Smart enough to hack the silly description, not smart enough to hack the checksum.",
            }
            raise Invalid(self.__class__.__name__, values, state, error_dict=error_dict)

class OtherValidator(validators.String):
    def __init__(self, list, if_missing=None):
        super(self.__class__, self).__init__(if_missing=if_missing)
        self.__list = list
    def validate_python(self, value, state):
        if value is not None:
            for bad in self.__list:
                if bad in value.lower():
                    raise Invalid(value + ' -- Nice try!', value, state)

class ExistingPersonSchema(BaseSchema):
    company = validators.String()
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True, min=3, max=10)
    country = CountryValidator(not_empty=True)
    i_agree = validators.Bool(if_missing=False)
    chained_validators = [IAgreeValidator("i_agree")]

class RegistrationSchema(BaseSchema):
    over18 = validators.Int(min=0, max=1, not_empty=True)
    nick = validators.String(if_missing=None)
    shell = validators.String(if_missing=None)
    shelltext = OtherValidator(if_missing=None, list=('cmd', 'command'))
    editor = validators.String(if_missing=None)
    editortext = OtherValidator(if_missing=None, list=('word', 'write'))
    distro = validators.String(if_missing=None)
    distrotext = OtherValidator(if_missing=None, list=('window', 'xp', 'vista'))
    vcs = validators.String(if_missing=None)
    vcstext = OtherValidator(if_missing=None, list=('visual sourcesafe', 'bitkeeper'))
    silly_description = validators.String(if_missing=None)
    silly_description_checksum = validators.String(if_missing=None, strip=True)
    if Config.get('pgp_collection', category='rego') != 'no':
        keyid = validators.String()
    planetfeed = validators.String(if_missing=None)
    voucher_code = VoucherValidator(if_empty=None)
    diet = validators.String()
    special = validators.String()
    signup = DictSet(if_missing=None)
    prevlca = DictSet(if_missing=None)

    chained_validators = [
        SillyDescriptionChecksum("silly_description", "silly_description_checksum"),
    ]

class SpecialOfferSchema(BaseSchema):
    name = validators.String()
    member_number = validators.String()

class NewRegistrationSchema(BaseSchema):
    person = ExistingPersonSchema()
    registration = RegistrationSchema()
    special_offer = SpecialOfferSchema()
    pre_validators = [NestedVariables]

class ProductUnavailable(Exception):
    """Exception when a product isn't available
    Attributes:
        product -- the product that wasn't available
    """

    def __init__(self, product):
        self.product = product

edit_schema = NewRegistrationSchema()

class RegistrationController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.is_activated_user)
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        c.product_categories = ProductCategory.find_all()
        c.ceilings = {}
        for ceiling in Ceiling.find_all():
            c.ceilings[ceiling.name] = ceiling

        self._generate_product_schema()
        c.products = Product.find_all()
        c.product_available = self._product_available
        c.able_to_edit = self._able_to_edit
        c.manual_invoice = self.manual_invoice
        c.signed_in_person = h.signed_in_person()

    def _able_to_edit(self):
        for invoice in h.signed_in_person().invoices:
            if not invoice.is_void:
                if invoice.is_paid and invoice.total != 0:
                    return False, "Sorry, you've already paid. Contact the team at " + Config.get('contact_email') + " if you need anything changed."
        return True, "You can edit"

    def _product_available(self, product, stock=True, qty=0):
        # bool stock: care about if the product is in stock (ie sold out?)
        if not product.available(stock, qty):
            return False
        if product.auth is not None:
            exec("auth = " + product.auth)
            if not auth:
                return False
        return True

    def _generate_product_schema(self):
        # Since the form is arbitrarily defined by what product types there are, the validation
        #   (aka schema) also needs to be dynamic.
        # Thus, this function generates a dynamic schema to validate a given set of products.
        #
        class ProductSchema(BaseSchema):
            # This schema is used to validate the products submitted by the
            # form.  It is populated below
            # EG:
            #   ProductSchema.add_field('count', validators.Int(min=1, max=100))
            # is the same as doing this inline:
            #   count = validators.Int(min=1, max=100)
            #
            # 2009-05-07 Josh H: Not sure why, but there is a reason this
            # class is declaired within this method and not earlier on
            # like in the voucher controller. Or maybe I just did this
            # poorly...
            pass

        # placed here so prevalidator can refer to it. This means we need a hacky method to save it :S
        ProductSchema.add_field('partner_name', validators.String(if_missing=None))
        ProductSchema.add_field('partner_email', validators.Email(if_missing=None))
        ProductSchema.add_field('partner_mobile', validators.String(if_missing=None))

        # Go through each category and each product and add generic validation
        for category in c.product_categories:
            clean_cat_name = category.clean_name()

            if category.display in ('radio', 'select'):
                # min/max can't be calculated on this form. You should only have 1 selected.
                ProductSchema.add_field('category_' + clean_cat_name, ProductInCategory(category=category, not_empty=True))
                for product in category.products:
                    if product.validate is not None:
                        validator = eval(product.validate)
                        validator.error_field_name = "error.%s" % category.clean_name()
                        ProductSchema.add_chained_validator(validator)
            elif category.display == 'checkbox':
                product_fields = []
                for product in category.products:
                    clean_prod_desc = product.clean_description()
                    product_field_name = 'product_' + clean_cat_name + '_' + clean_prod_desc + '_checkbox'

                    ProductSchema.add_field(product_field_name, CheckboxQty(product=product, if_missing=False))
                    product_fields.append(product_field_name)
                    if product.validate is not None:
                        validator = eval(product.validate)
                        validator.error_field_name = "error.%s" % category.clean_name()
                        ProductSchema.add_chained_validator(validator)
                validator = self.min_max_validator(product_fields, category)
                ProductSchema.add_chained_validator(validator)
            elif category.display == 'qty':
                # qty
                product_fields = []
                for product in category.products:
                    clean_prod_desc = product.clean_description()
                    product_field_name = 'product_' + clean_cat_name + '_' + clean_prod_desc + '_qty'

                    ProductSchema.add_field(product_field_name, ProductQty(product=product, if_missing=None))
                    product_fields.append(product_field_name)
                    if product.validate is not None:
                        validator = eval(product.validate)
                        validator.error_field_name = "error.%s" % category.clean_name()
                        ProductSchema.add_chained_validator(validator)
                validator = self.min_max_validator(product_fields, category)
                ProductSchema.add_chained_validator(validator)

        edit_schema.add_field('products', ProductSchema)

    @classmethod
    def min_max_validator(cls, fields, category):
        return ProductMinMax(
            product_fields=fields,
            min_qty=category.min_qty,
            max_qty=category.max_qty,
            category_name=category.name,
            error_field_name="error.%s" % category.clean_name())

    def is_speaker(self):
        try:
            return c.signed_in_person.is_speaker()
        except:
            return False

    def is_miniconf_org(self):
        try:
            return c.signed_in_person.is_miniconf_org()
        except:
            return False

    def is_volunteer(self,product):
        try:
            return c.signed_in_person and c.signed_in_person.volunteer and c.signed_in_person.volunteer.accepted and c.signed_in_person.volunteer.ticket_type == product
        except:
            return False

    def is_role(self, role):
        try:
            return c.signed_in_person.has_role(role)
        except:
            return False

    def is_same_person(self):
        return c.signed_in_person == c.registration.person

    @dispatch_on(POST="_new")
    def new(self):
        c.signed_in_person = h.signed_in_person()
        h.check_for_incomplete_profile(c.signed_in_person)

        if c.signed_in_person and c.signed_in_person.registration:
            redirect_to(action='edit', id=c.signed_in_person.registration.id)

        fields = dict(request.GET)
        c.special_offer = None
        if 'offer' in fields:
            c.special_offer = SpecialOffer.find_by_name(fields['offer'])
            if c.special_offer is not None:
                if c.special_offer.enabled:
                    # Create the special_registration record
                    special_registration = SpecialRegistration()
                    special_registration.special_offer_id = c.special_offer.id
                    special_registration.member_number = '' # TODO: switch to None
                    special_registration.person_id = c.signed_in_person.id
                    meta.Session.add(special_registration)
                    meta.Session.commit()
                else:
                    c.special_offer = None
        else:
            # The user alreay has used a special URL to register
            if c.signed_in_person.special_registration:
                c.special_offer = c.signed_in_person.special_registration[0].special_offer

        if c.special_offer is None and Config.get('conference_status') != 'open':
            if not h.auth.authorized(h.auth.has_organiser_role):
                redirect_to(action='status')
            else:
                # User is an organiser, so if the status is also 'debug' then they can register
                if Config.get('conference_status') != 'debug':
                    redirect_to(action='status')


        defaults = {}
        if Config.get('personal_info', category='rego')['home_address'] == 'no':
            defaults['person.address1'] = 'not available'
            defaults['person.city'] = 'not available'
            defaults['person.postcode'] = 'none'

        if c.signed_in_person:
            for k in ['address1', 'address2', 'city', 'state', 'postcode', 'country', 'phone', 'mobile', 'company', 'i_agree']:
                v = getattr(c.signed_in_person, k)
                if v is not None:
                    defaults['person.' + k] = getattr(c.signed_in_person, k)

        defaults['registration.signup.announce'] = 1
        defaults['registration.checkin'] = 17
        defaults['registration.checkout'] = 24

        #
        # Fugly hack.  If we aren't booking accommodation, then default the
        # product bought for Accommodation to 'I will organise my own'.
        #
        category = ProductCategory.find_by_name("Accommodation")
        if category and (len(category.products) == 0 or (len(category.products) == 1 and category.products[0].cost == 0)):
            field_name = 'products.category_%s' % category.name.replace("-","_")
            defaults[field_name] = category.products[0].id

        # Hacker-proof silly_description field
        c.silly_description, checksum = h.silly_description()
        defaults['registration.silly_description'] = c.silly_description
        defaults['registration.silly_description_checksum'] = checksum

        form = render("/registration/new.mako")
        return htmlfill.render(form, defaults)

    @validate(schema=edit_schema, form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        if c.signed_in_person and c.signed_in_person.registration:
            redirect_to(action='_edit', id=c.signed_in_person.registration.id)

        result = self.form_result

        c.special_offer = None
        if 'special_offer' in result:
            c.special_offer = SpecialOffer.find_by_name(result['special_offer']['name'])
            if c.special_offer is not None and not c.special_offer.enabled:
                c.special_offer = None

        if c.special_offer is None and Config.get('conference_status') != 'open':
            if not h.auth.authorized(h.auth.has_organiser_role):
                redirect_to(action='status')
            else:
                # User is an organiser, so if the status is also 'debug' then they can register
                if Config.get('conference_status') != 'debug':
                    redirect_to(action='status')


        # A blank registration
        c.registration = Registration()
        self.save_details(result)

        c.student_ticket = False
        c.infants = False
        c.children = False
        c.pp_children = False
        for rproduct in c.registration.products:
            if 'Ticket' in rproduct.product.category.name and 'Student' in rproduct.product.description:
                c.student_ticket = True
            elif 'Dinner' in rproduct.product.category.name:
                if 'Infant' == rproduct.product.description:
                    c.infants = True
                elif 'Child' == rproduct.product.description:
                    c.children = True
            elif rproduct.product.category.name == 'Partners Programme' and ('Child' in rproduct.product.description or 'Infant' in rproduct.product.description):
                c.pp_children = True

        email(
            c.person.email_address,
            render('registration/response.mako'))

        self.pay(c.registration.id, quiet=1)

        h.flash("Thank you for your registration!")
        if not c.person.paid():
            h.flash("To complete the registration process, please pay your invoice.")
        redirect_to(action='status')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_registration(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        # If we're an organiser, then don't check payment status.
        if not h.auth.authorized(h.auth.has_organiser_role):
            able, response = self._able_to_edit()
            if not able:
                c.error = response
                return render("/registration/error.mako")
        c.registration = Registration.find_by_id(id)
        defaults = {}
        defaults.update(h.object_to_defaults(c.registration, 'registration'))
        defaults.update(h.object_to_defaults(c.registration.person, 'person'))
        for rproduct in c.registration.products:
            product = rproduct.product
            category_name = product.category.clean_name()
            if product.category.display == 'checkbox':
                if product.available():
                    defaults['products.product_' + category_name + '_' + product.clean_description() + '_checkbox'] = '1'
            elif product.category.display == 'qty':
                if product.available() and rproduct.qty > 0:
                    defaults['products.product_' + category_name + '_' + product.clean_description() + '_qty'] = rproduct.qty
            else:
                if product.available():
                    defaults['products.category_' + category_name] = product.id

        # generate new silly description
        c.silly_description, checksum = h.silly_description()
        defaults['registration.silly_description'] = c.silly_description
        defaults['registration.silly_description_checksum'] = checksum

        # the partner fields are attached to the product in the form for some reason
        defaults['products.partner_name'] = c.registration.partner_name
        defaults['products.partner_email'] = c.registration.partner_email
        defaults['products.partner_mobile'] = c.registration.partner_mobile

        if c.registration.over18:
            defaults['registration.over18'] = 1
        else:
            defaults['registration.over18'] = 0

        if c.registration.shell in Config.get('shells', category='rego') or c.registration.shell == '':
            defaults['registration.shell'] = c.registration.shell
        else:
            defaults['registration.shell'] = 'other'
            defaults['registration.shelltext'] = c.registration.shell

        if c.registration.editor in Config.get('editors', category='rego') or c.registration.editor == '':
            defaults['registration.editor'] = c.registration.editor
        else:
            defaults['registration.editor'] = 'other'
            defaults['registration.editortext'] = c.registration.editor

        if c.registration.distro in Config.get('distros', category='rego') or c.registration.distro == '':
            defaults['registration.distro'] = c.registration.distro
        else:
            defaults['registration.distro'] = 'other'
            defaults['registration.distrotext'] = c.registration.distro
        if c.registration.vcs in Config.get('vcses', category='rego'):
            defaults['registration.vcs'] = c.registration.vcs
        else:
            defaults['registration.vcs'] = 'other'
            defaults['registration.vcstext'] = c.registration.vcs

        form = render('/registration/edit.mako')
        if c.form_errors:
            return form
        else:
            return htmlfill.render(form, defaults)

    @validate(schema=edit_schema, form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_registration(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.registration = Registration.find_by_id(id)
        result = self.form_result
        c.special_offer = None
        self.save_details(result)

        self.pay(c.registration.id, quiet=1)

        h.flash("Thank you for updating your registration!")
        if not c.person.paid():
            #h.flash("To complete the registration process, please pay your invoice.")
            redirect_to(controller='registration', action='pay', id=c.registration.id)
        redirect_to(action='status')

    def save_details(self, result):
        # Store Registration details
        for k in result['registration']:
            if k in ('shell', 'editor', 'distro', 'vcs'):
                if result['registration'][k] == 'other':
                    setattr(c.registration, k, result['registration'][k + 'text'])
                else:
                    setattr(c.registration, k, result['registration'][k])
            else:
                setattr(c.registration, k, result['registration'][k])

        if result['registration']['over18'] == 1:
            setattr(c.registration, 'over18', True)
        else:
            setattr(c.registration, 'over18', False)

        # hacky method to make validating sane
        setattr(c.registration, 'partner_name', result['products']['partner_name'])
        setattr(c.registration, 'partner_email', result['products']['partner_email'])
        setattr(c.registration, 'partner_mobile', result['products']['partner_mobile'])

        # Check whether we're already signed in or not, and store person details
        if c.registration.person:
            c.person = c.registration.person
        else:
            c.person = c.signed_in_person

        for k in result['person']:
            setattr(c.person, k, result['person'][k])

        # Create person<->registration relationship
        c.registration.person = c.person

        # Deal with the special offer if any
        if c.special_offer is not None:
            special_registration = SpecialRegistration.find_by_person_and_offer(c.person.id, c.special_offer.id)
            special_registration.member_number = result['special_offer']['member_number']
            meta.Session.add(special_registration)

        # Always delete the current products
        c.registration.products = []

        # Store Product details
        for category in c.product_categories:
            clean_cat_name = category.clean_name()
            if category.display in ('radio', 'select'):
                #product = Product.find_by_cat_and_desc(category.id, result['products']['category_' + clean_cat_name])
                product = Product.find_by_id(result['products']['category_' + clean_cat_name])
                if product != None:
                    rego_product = RegistrationProduct()
                    rego_product.registration = c.registration
                    rego_product.product = product
                    #if product.category.name == 'Accommodation':
                    #    rego_product.qty = c.registration.checkout - c.registration.checkin
                    #else:
                    #    rego_product.qty = 1
                    rego_product.qty = 1
                    c.registration.products.append(rego_product)
            elif category.display == 'checkbox':
                for product in category.products:
                    clean_prod_desc = product.clean_description()

                    if result['products']['product_' + clean_cat_name  + '_' + clean_prod_desc + '_checkbox']:
                        rego_product = RegistrationProduct()
                        rego_product.registration = c.registration
                        rego_product.product = product
                        rego_product.qty = 1
                        c.registration.products.append(rego_product)
            elif category.display == 'qty':
                for product in category.products:
                    clean_prod_desc = product.clean_description()

                    if result['products']['product_' + clean_cat_name + '_' + clean_prod_desc + '_qty'] not in [0, None]:
                        rego_product = RegistrationProduct()
                        rego_product.registration = c.registration
                        rego_product.product = product
                        rego_product.qty = result['products']['product_' + clean_cat_name + '_' + clean_prod_desc + '_qty']
                        c.registration.products.append(rego_product)

        meta.Session.commit()

    def status(self, id=0):
        if int(id) == 0:
            if h.signed_in_person() and h.signed_in_person().registration:
                c.registration = h.signed_in_person().registration
            else:
                c.registration = None
        else:
            if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_registration(id), h.auth.has_organiser_role)):
                # Raise a no_auth error
                h.auth.no_role()
            c.registration = Registration.find_by_id(id, abort_404 = False)

        if c.registration is None:
          c.person = h.signed_in_person()
        else:
          c.person = c.registration.person

        return render("/registration/status.mako")

    def pay(self, id, quiet=0):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_registration(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()
        registration = Registration.find_by_id(id)

        # Checks all existing invoices and invalidates them if a product is not available
        self.check_invoices(registration.person.invoices)

        # If we have a manual invoice, don't try and re-generate invoices
        if not self.manual_invoice(registration.person.invoices):

            try:
                invoice = self._create_invoice(registration)
            except ProductUnavailable, inst:
                if quiet: return
                c.product = inst.product
                c.registration = registration
                return render('/registration/product_unavailable.mako')

            if registration.voucher:
                self.apply_voucher(invoice, registration.voucher)

            # complicated check to see whether invoice is already in the system
            new_invoice = invoice
            for old_invoice in registration.person.invoices:
                if old_invoice != new_invoice and not old_invoice.manual and not old_invoice.is_void:
                    if self.invoices_identical(old_invoice, new_invoice):
                        invoice = old_invoice
                        if not quiet:
                            redirect_to(controller='invoice', action='view', id=invoice.id)
                        meta.Session.rollback()
                        return
                    if old_invoice.due_date < new_invoice.due_date:
                        new_invoice.due_date = old_invoice.due_date
                    old_invoice.void = "Registration Change"

            invoice.last_modification_timestamp = datetime.datetime.now()
            meta.Session.commit()

            if quiet: return
            redirect_to(controller='invoice', action='view', id=invoice.id)
        else:
            redirect_to(action='status')

    def check_invoices(self, invoices):
        for invoice in invoices:
            if not invoice.is_void and not invoice.manual and not invoice.is_paid:
                for ii in invoice.items:
                    if ii.product and not self._product_available(ii.product, True, ii.qty):
                        invoice.void = "Product " + ii.product.category.name + " - " + ii.product.description + " is no longer available"
                        meta.Session.commit()

    def manual_invoice(self, invoices):
        for invoice in invoices:
            if not invoice.is_void and invoice.manual:
                return True
        return False

    def invoices_identical(self, invoice1, invoice2):
        if invoice1.total == invoice2.total:
            if len(invoice1.items) == len(invoice2.items):
                matched_products = 0
                invoice1_matched_items = dict()
                invoice2_matched_items = dict()
                for invoice1_item in invoice1.items:
                    if invoice1_item.id in invoice1_matched_items:
                        continue
                    for invoice2_item in invoice2.items:
                        if invoice2_item.id in invoice2_matched_items:
                            continue
                        if invoice1_item.product == invoice2_item.product and invoice1_item.description == invoice2_item.description and invoice1_item.qty == invoice2_item.qty and invoice1_item.cost == invoice2_item.cost:
                            invoice1_matched_items[invoice1_item.id] = True
                            invoice2_matched_items[invoice2_item.id] = True
                            matched_products += 1
                            break
                if len(invoice1.items) == matched_products:
                    return True
        return False

    def _create_invoice(self, registration):
        # Create Invoice
        invoice = Invoice()
        invoice.person = registration.person
        invoice.manual = False
        invoice.void = None

        # Loop over the registration products and add them to the invoice.
        for rproduct in registration.products:
            if self._product_available(rproduct.product, True, rproduct.qty):
                ii = InvoiceItem(description=rproduct.product.category.name + ' - ' + rproduct.product.description, qty=rproduct.qty, cost=rproduct.product.cost)
                ii.invoice = invoice # automatically appends ii to invoice.items
                ii.product = rproduct.product
                product_expires = rproduct.product.available_until()
                if product_expires is not None:
                    if invoice.due_date is None or product_expires < invoice.due_date:
                        invoice.due_date = product_expires
                meta.Session.add(ii)
            else:
                for ii in invoice.items:
                    meta.Session.expunge(ii)
                meta.Session.expunge(invoice)
                raise ProductUnavailable(rproduct.product)

        # Some products might in turn include other products.  So the same
        # product might be available multiple times.  Work out all the
        # freebies first.
        included = {}
        included_products = {}
        freebies = {}
        for ii in invoice.items:
            if ii.product and ii.product.included:
                for iproduct in ii.product.included:
                    if iproduct.include_category.id not in included:
                        included[iproduct.include_category.id] = 0
                    included[iproduct.include_category.id] += iproduct.include_qty
                    freebies[iproduct.include_category.id] = 0
                    included_products[iproduct.include_category.id] = iproduct.include_category

        prices   = {}
        # Check for included products
        for ii in invoice.items:
            if ii.product and ii.product.category.id in included:
                if ii.product.category.id not in prices:
                    prices[ii.product.category.id] = []

                if included[ii.product.category.id] >= ii.qty:
                    prices[ii.product.category.id].append(ii.qty * ii.product.cost)
                    ii.free_qty = ii.qty

                    freebies[ii.product.category.id] += ii.qty
                    included[ii.product.category.id] -= ii.qty
                elif included[ii.product.category.id] > 0:
                    prices[ii.product.category.id].append(included[ii.product.category.id] * ii.product.cost)
                    ii.free_qty = included[ii.product.category.id]

                    freebies[ii.product.category.id] = included[ii.product.category.id]
                    included[ii.product.category.id] = 0

        for freebie in freebies:
            free_cost = 0
            if freebie in prices:
                for price in prices[freebie]:
                    free_cost += price

            # We have included products, create a discount for the cost of them.
            # This is not perfect, products of different prices can be discounted,
            # and it can either favor the customer or LCA, depending on the order
            # of items on the invoice
            if free_cost > 0:
                discount_item = InvoiceItem(description="Discount for " + str(freebies[freebie]) + " included " + included_products[freebie].name, qty=1, cost=-free_cost)
                invoice.items.append(discount_item)
                meta.Session.add(discount_item)

        meta.Session.add(invoice)
        return invoice

    def apply_voucher(self, invoice, voucher):
        # Voucher code calculation
        for vproduct in voucher.products:
            for ii in invoice.items:
                # if we have a category match
                if ii.product and ii.product.category == vproduct.product.category:
                    # The qty we will give
                    if ii.qty < vproduct.qty:
                        qty = ii.qty
                    else:
                        qty = vproduct.qty

                    # the discount we will give
                    max_discount = vproduct.product.cost * vproduct.percentage / 100
                    if ii.product.cost >= max_discount:
                        discount = max_discount
                    else:
                        discount = ii.product.cost
                    discount_item = InvoiceItem(description="Discount Voucher (" + voucher.comment + ") for " + vproduct.product.description, qty=qty, cost=-discount)
                    meta.Session.add(discount_item)
                    invoice.items.append(discount_item)
                    break

    @authorize(h.auth.has_organiser_role)
    def index(self):
        per_page = 20
        from webhelpers import paginate #Upgrade to new paginate

        filter = dict(request.GET)
        filter['role'] = []
        for key,value in request.GET.items():
            if key == 'role': filter['role'].append(value)
        filter['product'] = []
        for key,value in request.GET.items():
            if key == 'product': filter['product'].append(value)

        """
        registration_list = self.dbsession.query(self.model).order_by(self.model.c.id)
        if filter.has_key('role'):
            role_name = filter['role']
            if role_name == 'speaker':
                registration_list = registration_list.select_from(registration_tables.registration.join(core_tables.person)).filter(model.Person.proposals.any(accepted='1'))
            elif role_name == 'miniconf':
                registration_list = registration_list.select_from(registration_tables.registration.join(core_tables.person)).filter(model.Person.proposals.any(accepted='1'))
            elif role_name == 'volunteer':
                pass
            elif role_name != 'all':
                registration_list = registration_list.select_from(registration_tables.registration.join(core_tables.person)).filter(model.Person.roles.any(name=role_name))
        """

        if (len(filter) in [2,3,4] and filter.has_key('per_page') and (len(filter['role']) == 0 or 'all' in filter['role']) and filter['status'] == 'all' and (len(filter['product']) == 0 or 'all' in filter['product'])) or len(filter) < 2:
            # no actual filters to apply besides per_page, so we can get paginate to do the query
            registration_list = meta.Session.query(Registration).order_by(Registration.id).all()
        else:
            import copy
            registration_list_full = Registration.find_all()
            registration_list = copy.copy(registration_list_full)

            for registration in registration_list_full:
                if 'speaker' in filter['role'] and registration.person.is_speaker() is not True:
                    registration_list.remove(registration)
                elif 'miniconf' in filter['role'] and registration.person.is_miniconf_org() is not True:
                    registration_list.remove(registration)
                elif 'volunteer' in filter['role'] and registration.person.is_volunteer() is not True:
                    registration_list.remove(registration)
                elif (len(filter['role']) - len(set(filter['role']) & set(['all', 'speaker', 'miniconf', 'volunteer']))) != 0 and len(set(filter['role']) & set([role.name for role in registration.person.roles])) == 0:
                    registration_list.remove(registration)
                elif filter.has_key('status') and filter['status'] == 'paid' and not registration.person.paid():
                    registration_list.remove(registration)
                elif filter.has_key('status') and filter['status'] == 'unpaid' and registration.person.paid():
                    registration_list.remove(registration)
                elif filter.has_key('diet') and filter['diet'] == 'true' and (registration.diet == '' or registration.diet.lower() in ('n/a', 'none', 'nill', 'nil', 'no')):
                    registration_list.remove(registration)
                elif filter.has_key('special_needs') and filter['special_needs'] == 'true' and (registration.special == '' or registration.special.lower() in ('n/a', 'none', 'nill', 'nil', 'no')):
                    registration_list.remove(registration)
                elif filter.has_key('notes') and filter['notes'] == 'true' and len(registration.notes) == 0:
                    registration_list.remove(registration)
                elif filter.has_key('under18') and filter['under18'] == 'true' and registration.over18:
                    registration_list.remove(registration)
                elif filter.has_key('voucher') and filter['voucher'] == 'true' and not registration.voucher:
                    registration_list.remove(registration)
                elif filter.has_key('manual_invoice') and filter['manual_invoice'] == 'true' and not (True in [invoice.manual for invoice in registration.person.invoices]):
                    registration_list.remove(registration)
                elif filter.has_key('not_australian') and filter['not_australian'] == 'true' and registration.person.country == "AUSTRALIA":
                    registration_list.remove(registration)
                elif len(filter['product']) > 0 and 'all' not in filter['product']:
                    # has to be done last as it is an OR not an AND
                    valid_invoices = []
                    for invoice in registration.person.invoices:
                        if not invoice.is_void:
                            valid_invoices.append(invoice)
                    if len(set([int(id) for id in filter['product']]) & set([x for subL in [[item.product_id for item in invoice.items] for invoice in valid_invoices] for x in subL])) == 0:
                       registration_list.remove(registration)

        if filter.has_key('export') and filter['export'] == 'true':
            return self._export_list(registration_list)

        if filter.has_key('per_page'):
            try:
                per_page = int(filter['per_page'])
            except:
                pass

        if filter.has_key('page'):
            page = int(filter['page'])
        else:
            page = 1

        setattr(c, 'per_page', per_page)
        pagination =  paginate.Page(registration_list, per_page = per_page, page = page)
        setattr(c, 'registration_pages', pagination)
        setattr(c, 'registration_collection', pagination.items)
        setattr(c, 'registration_request', filter)

        setattr(c, 'roles', Role.find_all())
        setattr(c, 'product_categories', ProductCategory.find_all())

        return render('/registration/list.mako')

    def _export_list(self, registration_list):
        columns = ['Rego', 'Firstname', 'Lastname', 'Email', 'Nick', 'Company', 'State', 'Country', 'Valid Invoices', 'Paid for Products', 'Accommodation', 'Speaker', 'Miniconf Org', 'Volunteer', 'Role(s)', 'Diet', 'Special Needs', 'Silly Description', 'Over 18']
        if type(registration_list) is not list:
            registration_list = registration_list.all()

        data = []
        for registration in registration_list:
            products = []
            invoices = []
            accommodation = []

            for product in registration.products:
                if product.product.category.name.lower() == "accommodation":
                    accommodation.append(product.product.description)

            for invoice in registration.person.invoices:
                if invoice.is_paid and not invoice.is_void:
                    invoices.append(str(invoice.id))
                    for item in invoice.items:
                        products.append(str(item.qty) + "x" + item.description)

            # Hack to fix mising fields
            if not registration.nick:
                registration.nick = ''
            if not registration.silly_description:
                registration.silly_description = ''

            data.append([registration.id,
                         registration.person.firstname.encode('utf-8'),
                         registration.person.lastname.encode('utf-8'),
                         registration.person.email_address.encode('utf-8'),
                         registration.nick.encode('utf-8'),
                         registration.person.company.encode('utf-8'),
                         registration.person.state.encode('utf-8'),
                         registration.person.country.encode('utf-8'),
                         ", ".join(invoices).encode('utf-8'),
                         ", ".join(products).encode('utf-8'),
                         ", ".join(accommodation).encode('utf-8'),
                         #registration.checkin,
                         #registration.checkout,
                         registration.person.is_speaker(),
                         registration.person.is_miniconf_org(),
                         registration.person.is_volunteer(),
                         ", ".join([role.name for role in registration.person.roles]),
                         registration.diet.encode('utf-8'),
                         registration.special.encode('utf-8'),
                         registration.silly_description.encode('utf-8'),
                         registration.over18])


        import csv, StringIO
        f = StringIO.StringIO()
        w = csv.writer(f)
        w.writerow(columns)
        w.writerows(data)
        res = Response(f.getvalue())
        res.headers['Content-type']='text/plain; charset=utf-8'
        res.headers['Content-Disposition']='attachment; filename="table.csv"'
        return res

    @authorize(h.auth.has_organiser_role)
    def generate_badges(self):
        defaults = dict(request.POST)
        stamp = False
        if defaults.has_key('stamp') and defaults['stamp']:
            stamp = defaults['stamp']
        c.text = ''
        data = []
        if request.method == 'POST' and defaults:
            if defaults['reg_id'] != '':
                reg_id_list = defaults['reg_id'].split("\n")
                regos = [(r.person.lastname.lower(), r.person.firstname.lower(), r)
                         for r in Registration.find_by_ids(reg_id_list)]
                regos.sort()
                registration_list = [row[-1] for row in regos]

                if len(registration_list) != len(reg_id_list):
                    c.text = 'Registration ID not found. Please check the <a href="/registration">registration list</a>.'
                    return render('registration/generate_badges.mako')
                else:
                    for registration in registration_list:
                        data.append(self._registration_badge_data(registration, stamp))
                        registration.person.badge_printed = True
            else:
                regos = [(r.person.lastname.lower(), r.person.firstname.lower(), r)
                         for r in Registration.find_all()]
                regos.sort()
                registration_list = [row[-1] for row in regos]

                for registration in registration_list:
                    append = False
                    if registration.person.has_paid_ticket() and not registration.person.badge_printed:
                        if defaults['type'] == 'all':
                            append = True
                        else:
                            for invoice in registration.person.invoices:
                                if invoice.is_paid and not invoice.is_void:
                                    for item in invoice.items:
                                        if defaults['type'] == 'concession' and item.description.startswith('Concession'):
                                            append = True
                                        elif defaults['type'] == 'hobby' and (item.description.find('Hobbyist') > -1 or item.description.find('Hobbiest') > -1):
                                            append = True
                                        elif defaults['type'] == 'professional' and (item.description.find('Professional') > -1 or item.description.startswith('Karoro')):
                                            append = True
                                        elif defaults['type'] == 'press' and item.description.startswith('Press'):
                                            append = True
                                        elif defaults['type'] == 'organiser' and item.description.startswith('Organiser'):
                                            append = True
                                        elif defaults['type'] == 'monday_tuesday' and item.description.find('Monday + Tuesday') > -1:
                                            append = True
                            if defaults['type'] == 'speaker' and registration.person.is_speaker():
                                append = True
                            elif defaults['type'] == 'mc_organiser' and registration.person.is_miniconf_org():
                                append = True
                            elif defaults['type'] == 'volunteer' and registration.person.is_volunteer():
                                append = True
                        if append:
                            data.append(self._registration_badge_data(registration, stamp))
                            registration.person.badge_printed = True

            meta.Session.commit() # save badge printed data
            setattr(c, 'data', data)

            import os, tempfile
            c.index = 0
            files = []
            while c.index < len(c.data):
                while c.index + 4 > len(c.data):
                    c.data.append(self._registration_badge_data(False))
                res = render('registration/badges_svg.mako')
                (svg_fd, svg) = tempfile.mkstemp('.svg')
                svg_f = os.fdopen(svg_fd, 'w')
                svg_f.write(res)
                svg_f.close()
                files.append(svg)
                c.index += 4

            (tar_fd, tar) = tempfile.mkstemp('.tar.gz')
            os.close(tar_fd)
            os.system('tar -zcvf %s %s' % (tar, " ".join(files)))

            tar_f = file(tar)
            res = Response(tar_f.read())
            tar_f.close()
            res.headers['Content-type'] = 'application/octet-stream'
            res.headers['Content-Disposition'] = ( 'attachment; filename=badges.tar.gz' )
            return res
        return render('registration/generate_badges.mako')

    def _registration_badge_data(self, registration, stamp = False):
        if registration:
            dinner_tickets = 0
            speakers_tickets = 0
            breakfast = 0
            pdns_ticket = False
            ticket = ''
            for invoice in registration.person.invoices:
                if invoice.is_paid and not invoice.is_void:
                    for item in invoice.items:
                        if item.description.startswith('Penguin Dinner'):
                            dinner_tickets += item.qty
                        elif item.description.startswith('Speakers Dinner'):
                            speakers_tickets += item.qty
                        elif item.description.find('Student') > -1:
                            ticket = 'Hobbyist'
                        elif item.description.find('Hobbyist') > -1:
                            ticket = 'Hobbyist'
                        elif item.description.find('Professional') > -1 or item.description.find('Korora') > -1:
                            ticket = 'Professional'
                            pdns_ticket = True
                        elif item.description.find('Press') > -1:
                            ticket = 'Press'
                            pdns_ticket = True
                        elif item.description.startswith('Organiser'):
                            ticket = 'Organiser'
                            pdns_ticket = True
                        elif item.description.find('Miniconf-Only') > -1 or item.description.find('Minconf-Only') > -1:
                            ticket = 'Miniconfs Only'
                        elif item.description.find('Fairy Penguin Sponsor') > -1 or item.description.find('Fairy Penguin Sponsor') > -1:
                            ticket = 'Sponsor'
                        elif item.description.find('reakfast') > -1:
                            breakfast += item.qty
            if registration.person.has_role('core_team'):
                ticket = 'Organiser'
            elif registration.person.is_speaker():
                ticket = 'Speaker'
                pdns_ticket = True
            elif registration.person.is_miniconf_org():
                ticket = 'Miniconf Organiser'
                pdns_ticket = True
            elif registration.person.is_volunteer():
                ticket = 'Volunteer'

            region = 'world'
            if registration.person.country.strip().lower() == 'australia' and registration.person.state.strip().lower() in ['tas', 'tasmania']:
                region = 'tasmania'
            elif registration.person.country.strip().lower() == 'australia':
                region = 'australia'
            elif registration.person.country.strip().lower() == 'switzerland':
                region = 'switzerland'
            elif registration.person.country.strip().lower() == 'canada':
                region = 'canada'
            elif registration.person.country.strip().lower() == 'finland':
                region = 'finland'
            elif registration.person.country.strip().lower() == 'norway':
                region = 'norway'
            elif registration.person.country.strip().lower() in ['new zealand', 'nz']:
                region = 'new_zealand'

            favourites = []
            if registration.shell != '':
                favourites.append(self._sanitise_badge_field(registration.shell))
            if registration.editor != '':
                favourites.append(self._sanitise_badge_field(registration.editor))
            if registration.distro != '':
                favourites.append(self._sanitise_badge_field(registration.distro))

            data = { 'ticket': ticket,
                     'firstname' : self._sanitise_badge_field(registration.person.firstname),
                     'lastname' : self._sanitise_badge_field(registration.person.lastname),
                     'nickname': self._sanitise_badge_field(registration.nick),
                     'company': self._sanitise_badge_field(registration.person.company),
                     'favourites': ", ".join(favourites),
                     'region': region,
                     'dinner_tickets': dinner_tickets,
                     'speakers_tickets': speakers_tickets,
                     'pdns_ticket' : pdns_ticket,
                     'over18': registration.over18,
                     'silly': self._sanitise_badge_field(registration.silly_description),
                     'breakfast': breakfast

            }

            # For some reason some keys are None even if pgp_collection is yes, should probably fix the real problem.
            if Config.get('pgp_collection', category='rego') != 'no' and registration.keyid:
                    data['gpg'] = self._sanitise_badge_field(registration.keyid)
            return data
        return {'ticket': '', 'firstname': '', 'lastname': '', 'nickname': '', 'company': '', 'favourites': '', 'gpg': '', 'region': '', 'dinner_tickets': 0, 'speakers_tickets': 0, 'pdns_ticket' : False, 'over18': True, 'silly': '','breakfast': 0}

    def _sanitise_badge_field(self, field):
        disallowed_chars = re.compile(r'(\n|\r\n|\t)')
        return disallowed_chars.sub(' ', h.escape(field.strip()))

    def view(self, id):
        # We need to recheck auth in here so we can pass in the id
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_registration(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.registration = Registration.find_by_id(id)
        return render('/registration/view.mako')

    @authorize(h.auth.has_organiser_role)
    def remind(self):
        c.registration_collection = Registration.find_all()
        return render('/registration/remind.mako')

    @authorize(h.auth.has_organiser_role)
    def professionals_latex(self):
        c.profs= {}
        registration_list = Registration.find_all()
        for r in registration_list:
            is_prof = False
            for invoice in r.person.invoices:
                if invoice.is_paid and not invoice.is_void:
                    if r.person.is_speaker() or r.person.is_miniconf_org():
                        is_prof = True
                    else:
                        for item in invoice.items:
                            if (item.description.find('Professional') > -1 or item.description.find('Little Blue') > -1):
                               is_prof = True

            if is_prof:
                if r.person.company not in c.profs:
                     c.profs[r.person.company] = {}
                if r.person.lastname not in c.profs[r.person.company]:
                    c.profs[r.person.company][r.person.lastname] = []
                c.profs[r.person.company][r.person.lastname].append(r.person.fullname)

        response.headers['Content-type']='text/plain; charset=utf-8'
        return render('/registration/professionals_latex.mako')

    @authorize(h.auth.has_organiser_role)
    def rego_desk_latex(self):
        registration_list = Registration.find_all()
        for r in registration_list:
            if r.person.is_professional():
                if r.person.company not in c.profs:
                     c.profs[r.person.company] = {}
                if r.person.lastname not in c.profs[r.person.company]:
                    c.profs[r.person.company][r.person.lastname] = []
                c.profs[r.person.company][r.person.lastname].append(r.person.fullname)

        response.headers['Content-type']='text/plain; charset=utf-8'
