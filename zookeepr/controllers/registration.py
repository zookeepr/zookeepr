# coding=utf-8
import logging
import re

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, Response
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, DictSet, ProductInCategory
from zookeepr.lib.validators import ProductQty, ProductMinMax, CheckAccomDates
from zookeepr.lib.validators import PrevLCAValidator

# validators used from the database
from zookeepr.lib.validators import ProDinner, PPDetails, PPChildrenAdult

import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Registration, Role, RegistrationProduct, Person
from zookeepr.model import ProductCategory, Product, Voucher, Ceiling
from zookeepr.model import Invoice, InvoiceItem
from zookeepr.model.special_offer import SpecialOffer
from zookeepr.model.special_registration import SpecialRegistration

from zookeepr.config.lca_info import lca_info, lca_rego

from zookeepr.controllers.person import PersonSchema

log = logging.getLogger(__name__)

import datetime

class NotExistingRegistrationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        rego = None
        if 'signed_in_person_id' in session:
            rego = state.query(model.Registration).filter_by(person_id=session['signed_in_person_id']).first()
        if rego is not None and rego != c.registration:
            raise Invalid("Thanks for your keenness, but you've already registered!", value, state)

class DuplicateVoucherValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        voucher = Voucher.find_by_code(value['voucher_code'])
        if voucher != None:
            if voucher.registration:
                if voucher.registration[0].person.id != h.signed_in_person().id:
                    raise Invalid("Voucher code already in use!", value, state)
        elif value['voucher_code']:
            raise Invalid("Unknown voucher code!", value, state)

class SillyDescriptionChecksum(validators.FancyValidator):
    def validate_python(self, value, state):
        checksum = h.silly_description_checksum(value['silly_description'])
        if value['silly_description_checksum'] != checksum:
            raise Invalid("Smart enough to hack the silly description, not smart enough to hack the checksum.", value, state)

class IAgreeValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        if not value['i_agree']:
            raise Invalid("You must read and accept the terms and conditions before you can register.", value, state)

class PrevLCAValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        if value['prevlca'] is not None and '00' in value['prevlca']:
            raise Invalid("LCA in Auckland -- Yeah Right.", value, state)

class ShellValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        if value['shelltext'] is not None and value['shell'] == 'other':
            if value['shelltext'].lower() == 'cmd.exe' or value['shelltext'].lower() == 'command.com':
                raise Invalid(value['shelltext'].lower() + ' -- Nice try!', value, state)

class ExistingPersonSchema(BaseSchema):
    company = validators.String()
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True)
    country = validators.String(not_empty=True)

class RegistrationSchema(BaseSchema):
    over18 = validators.Int(min=0, max=1, not_empty=True)
    nick = validators.String()
    shell = validators.String()
    shelltext = validators.String()
    editor = validators.String()
    editortext = validators.String()
    distro = validators.String()
    distrotext = validators.String()
    silly_description = validators.String()
    silly_description_checksum = validators.String(strip=True)
    if lca_rego['pgp_collection'] != 'no':
        keyid = validators.String()
    planetfeed = validators.String()
    voucher_code = validators.String(if_empty=None)
    diet = validators.String()
    special = validators.String()
    checkin = validators.Int(min=0, max=31)
    checkout = validators.Int(min=0, max=31)
    signup = DictSet(if_missing=None)
    prevlca = DictSet(if_missing=None)
    miniconf = DictSet(if_missing=None)
    i_agree = validators.Bool(if_missing=False)

    chained_validators = [CheckAccomDates(), SillyDescriptionChecksum(), DuplicateVoucherValidator(), IAgreeValidator(), PrevLCAValidator(), ShellValidator()]

class SpecialOfferSchema(BaseSchema):
    name = validators.String()
    member_number = validators.String()

class NewRegistrationSchema(BaseSchema):
    person = ExistingPersonSchema()
    registration = RegistrationSchema()
    special_offer = SpecialOfferSchema()

    chained_validators = [NotExistingRegistrationValidator()]
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
            if not invoice.is_void():
                if invoice.paid() and invoice.total() != 0:
                    return False, "Sorry, you've already paid. Contact the team at " + h.lca_info['contact_email'] + " if you need anything changed."
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
            # This schema is used to validate the products submitted by the form.
            # It is populated below
            # EG:
            #   ProductSchema.add_field('count', validators.Int(min=1, max=100))
            # is the same as doing this inline:
            #   count = validators.Int(min=1, max=100)
            
            # 2009-05-07 Josh H: Not sure why, but there is a reason this class is declaired within this method and not earlier on like in the voucher controller. Or maybe I just did this poorly...
            pass

        # placed here so prevalidator can refer to it. This means we need a hacky method to save it :S
        ProductSchema.add_field('partner_name', validators.String())
        ProductSchema.add_field('partner_email', validators.Email())
        ProductSchema.add_field('partner_mobile', validators.String())
        
        # Go through each category and each product and add generic validation
        for category in c.product_categories:
            clean_cat_name = category.clean_name()

            if category.display in ('radio', 'select'):
                # min/max can't be calculated on this form. You should only have 1 selected.
                ProductSchema.add_field('category_' + clean_cat_name, ProductInCategory(category=category, not_empty=True))
                for product in category.products:
                    if product.validate is not None:
                        exec("validator = " + product.validate)
                        ProductSchema.add_pre_validator(validator)
            elif category.display == 'checkbox':
                product_fields = []
                for product in category.products:
                    clean_prod_desc = product.clean_description()
                    #if self._product_available(product):
                    ProductSchema.add_field('product_' + clean_cat_name, validators.Bool(if_missing=False)) # TODO: checkbox available() not implemented. See lib.validators.ProductCheckbox.
                    product_fields.append('product_' + clean_cat_name)
                    if product.validate is not None:
                        exec("validator = " + product.validate)
                        ProductSchema.add_pre_validator(validator)
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
            elif category.display == 'qty':
                # qty
                product_fields = []
                for product in category.products:
                    clean_prod_desc = product.clean_description()
  
                    #if self._product_available(product):
                    ProductSchema.add_field('product_' + clean_cat_name + '_' + clean_prod_desc + '_qty', ProductQty(product=product, if_missing=None))
                    product_fields.append('product_' + clean_cat_name + '_' + clean_prod_desc+ '_qty')
                    if product.validate is not None:
                        exec("validator = " + product.validate)
                        ProductSchema.add_pre_validator(validator)

                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))

        edit_schema.add_field('products', ProductSchema)

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

    def is_volunteer(self):
        try:
            return c.signed_in_person.is_volunteer()
        except:
            return False

    def is_press(self):
        try:
            return c.signed_in_person.has_role('press')
        except:
            return False

    def is_same_person(self):
        return c.signed_in_person == c.registration.person

    @dispatch_on(POST="_new")
    def new(self):
        c.signed_in_person = h.signed_in_person()
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

        if c.special_offer is None and lca_info['conference_status'] is not 'open':
            redirect_to(action='status')

        defaults = {}
        if c.signed_in_person:
            for k in ['address1', 'address2', 'city', 'state', 'postcode', 'country', 'phone', 'mobile', 'company']:
                v = getattr(c.signed_in_person, k)
                if v is not None:
                    defaults['person.' + k] = getattr(c.signed_in_person, k)

        defaults['registration.signup.announce'] = 1
        defaults['registration.checkin'] = 17
        defaults['registration.checkout'] = 24

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
        
        if c.special_offer is None and lca_info['conference_status'] is not 'open':
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
            defaults['products.category_' + category_name] = product.id
            if rproduct.qty > 0:
                defaults['products.product_' + category_name + '_' + product.clean_description() + '_qty'] = rproduct.qty

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

        if c.registration.shell in lca_rego['shells']:
            defaults['registration.shell'] = c.registration.shell
        else:
            defaults['registration.shell'] = 'other'
            defaults['registration.shelltext'] = c.registration.shell
        if c.registration.editor in lca_rego['editors']:
            defaults['registration.editor'] = c.registration.editor
        else:
            defaults['registration.editor'] = 'other'
            defaults['registration.editortext'] = c.registration.editor
        if c.registration.distro in lca_rego['distros']:
            defaults['registration.distro'] = c.registration.distro
        else:
            defaults['registration.distro'] = 'other'
            defaults['registration.distrotext'] = c.registration.distro

        form = render('/registration/edit.mako')
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

        redirect_to(action='status')

    def save_details(self, result):
        # Store Registration details
        for k in result['registration']:
            if k in ('shell', 'editor', 'distro'):
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
                    if product.category.name == 'Accommodation':
                        rego_product.qty = c.registration.checkout - c.registration.checkin
                    else:
                        rego_product.qty = 1
                    c.registration.products.append(rego_product)
            elif category.display == 'checkbox':
                for product in category.products:
                    clean_prod_desc = product.clean_description()

                    if result['products']['product_' + clean_cat_name + '_' + clean_prod_desc] == True:
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
                if old_invoice != new_invoice and not old_invoice.manual and not old_invoice.is_void():
                    if self.invoices_identical(old_invoice, new_invoice):
                        invoice = old_invoice
                        meta.Session.clear()

                        if quiet: return
                        redirect_to(controller='invoice', action='view', id=invoice.id)
                    else:
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
            if not invoice.is_void() and not invoice.manual and not invoice.paid():
                for ii in invoice.items:
                    if ii.product and not self._product_available(ii.product, True, ii.qty):
                        invoice.void = "Product " + ii.product.category.name + " - " + ii.product.description + " is no longer available"

    def manual_invoice(self, invoices):
        for invoice in invoices:
            if not invoice.is_void() and invoice.manual:
                return True
        return False

    def invoices_identical(self, invoice1, invoice2):
        if invoice1.total() == invoice2.total():
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
                if ii.product.category == vproduct.product.category:
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
        #from zookeepr.model.core import tables as core_tables
        #from zookeepr.model.registration import tables as registration_tables
        #from zookeepr.model.proposal import tables as proposal_tables
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
                elif len(filter['product']) > 0 and 'all' not in filter['product']:
                    # has to be done last as it is an OR not an AND
                    valid_invoices = []
                    for invoice in registration.person.invoices:
                        if not invoice.is_void():
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
        columns = ['Rego', 'Name', 'Email', 'Company', 'State', 'Country', 'Valid Invoices', 'Paid for Products', 'checkin', 'checkout', 'days (checkout-checkin: should be same as accom qty.)', 'Speaker', 'Miniconf Org', 'Volunteer', 'Role(s)', 'Diet', 'Special Needs']
        if type(registration_list) is not list:
            registration_list = registration_list.all()
        
        data = []
        for registration in registration_list:
            products = []
            invoices = []
            for invoice in registration.person.invoices:
                if invoice.paid() and not invoice.is_void():
                    invoices.append(str(invoice.id))
                    for item in invoice.items:
                        products.append(str(item.qty) + "x" + item.description)
        
            data.append([registration.id,
                         registration.person.firstname + " " + registration.person.lastname,
                         registration.person.email_address,
                         registration.person.company,
                         registration.person.state,
                         registration.person.country,
                         ", ".join(invoices),
                         ", ".join(products),
                         registration.checkin,
                         registration.checkout,
                         (registration.checkout - registration.checkin),
                         registration.person.is_speaker(),
                         registration.person.is_miniconf_org(),
                         registration.person.is_volunteer(),
                         ", ".join([role.name for role in registration.person.roles]),
                         registration.diet,
                         registration.special,
                       ])
        
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
                #registration_list = self.dbsession.query(self.model).filter(model.Registration.id.in_(reg_id_list)).all()
                registration_list = self.dbsession.query(Registration).filter_by(id.in_(reg_id_list)).all()
                if len(registration_list) != len(reg_id_list):
                    c.text = 'Registration ID not found. Please check the <a href="/registration">registration list</a>.'
                    return render('registration/generate_badges.mako')
                else:
                    for registration in registration_list:
                        data.append(self._registration_badge_data(registration, stamp))
                        registration.person.badge_printed = True
            else:
                registration_list = Registration.find_all()
                for registration in registration_list:
                    append = False
                    if registration.person.has_paid_ticket() and not registration.person.badge_printed:
                        if defaults['type'] == 'all':
                            append = True
                        else:
                            for invoice in registration.person.invoices:
                                if invoice.paid() and not invoice.is_void():
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

            meta.Session.flush() # save badge printed data
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

            (tar_fd, tar) = tempfile.mkstemp('.tar')
            os.close(tar_fd)
            os.system('tar -cvf %s %s' % (tar, " ".join(files)))

            tar_f = file(tar)
            res = Response(tar_f.read())
            tar_f.close()
            res.headers['Content-type'] = 'application/octet-stream'
            res.headers['Content-Disposition'] = ( 'attachment; filename=badges.tar' )
            return res
        return render('registration/generate_badges.mako')

    def _registration_badge_data(self, registration, stamp = False):
        if registration:
            dinner_tickets = 0
            ticket = ''
            for invoice in registration.person.invoices:
                if invoice.paid() and not invoice.is_void():
                    for item in invoice.items:
                        if item.description.startswith('Penguin Dinner'):
                            dinner_tickets += item.qty
                        elif item.description.startswith('Concession'):
                            ticket = 'Concession'
                        elif item.description.find('Hobbyist') > -1 or item.description.find('Hobbiest') > -1:
                            ticket = 'Hobbyist'
                        elif (item.description.find('Professional') > -1 or item.description.startswith('Kororo')):
                            ticket = 'Professional'
                        elif item.description.startswith('Press'):
                            ticket = 'Press'
                        elif item.description.startswith('Organiser'):
                            ticket = 'Organiser'
                        elif item.description.find('Monday + Tuesday') > -1:
                            ticket = 'miniconfs Only'
            if registration.person.is_speaker():
                ticket = 'Speaker'
            elif registration.person.is_miniconf_org():
                ticket = 'miniconf Organiser'
            elif registration.person.is_volunteer():
                ticket = 'Volunteer'

            if not stamp:
                ticket = ''

            region = 'world'
            if registration.person.country.strip().lower() == 'australia' and registration.person.state.strip().lower() in ['tas', 'tasmania']:
                region = 'tasmania'
            elif registration.person.country.strip().lower() == 'australia':
                region = 'australia'
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
                     'name': self._sanitise_badge_field(registration.person.firstname + " " + registration.person.lastname),
                     'nickname': self._sanitise_badge_field(registration.nick),
                     'company': self._sanitise_badge_field(registration.person.company),
                     'favourites': ", ".join(favourites),
                     'region': region,
                     'dinner_tickets': dinner_tickets,
                     'over18': registration.over18,
                     'ghost': 'ghost' in [role.name for role in registration.person.roles],
                     'papers': 'reviewer' in [role.name for role in registration.person.roles],
                     'artist': 'artist' in [role.name for role in registration.person.roles],
                     'silly': self._sanitise_badge_field(registration.silly_description)
            }
            if lca_rego['pgp_collection'] != 'no':
                data['gpg'] = self._sanitise_badge_field(registration.keyid)
            return data
        return {'ticket': '', 'name': '', 'nickname': '', 'company': '', 'favourites': '', 'gpg': '', 'region': '', 'dinner_tickets': 0, 'over18': True, 'ghost': False, 'papers': False, 'artist': False, 'silly': ''}

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
