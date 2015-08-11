"""Populate database

Revision ID: 4ed1a2dd2573
Revises: 590a0265a5f
Create Date: 2015-08-04 14:29:52.468792

"""

# revision identifiers, used by Alembic.
revision = '4ed1a2dd2573'
down_revision = '590a0265a5f'

import datetime
import logging

from alembic import op
import sqlalchemy as sa


meta = sa.MetaData()
log = logging.getLogger('alembic.migration')

tables = [
    'role',
    'social_network',
    'product_category',
    'ceiling',
    'person',
    'person_role_map',
    'product',
    'product_ceiling_map',
    'accommodation_assistance_type',
    'target_audience',
    'proposal_type',
    'funding_type',
    'travel_assistance_type',
    'db_content_type',
    'special_offer',
    'funding_status',
    'proposal_status',
]

tables_delete_order = [
    'social_network',
    'person_role_map',
    'person',
    'role',
    'product_ceiling_map',
    'product_category',
    'ceiling',
    'product',
    'accommodation_assistance_type',
    'target_audience',
    'proposal_type',
    'funding_type',
    'travel_assistance_type',
    'db_content_type',
    'special_offer',
    'funding_status',
    'proposal_status',
]

data = {
    'role': [
        {
            'comment': 'Has full access to management pages',
            'pretty_name': 'Organizer', 'display_order': None,
            'name': 'organiser'
        },
        {'comment': 'Member of core team', 'pretty_name': 'Core Team',
         'display_order': None, 'name': 'team'},
        {'comment': 'Has access to the proposal review system',
         'pretty_name': 'Paper Reviewer', 'display_order': None,
         'name': 'reviewer'},
        {'comment': 'Is a miniconference organiser',
         'pretty_name': 'Miniconf Organiser', 'display_order': None,
         'name': 'miniconf'},
        {'comment': 'Has access to proposal review system management functions',
         'pretty_name': 'Papers Chair', 'display_order': None,
         'name': 'proposals_chair'},
        {'comment': 'Is allowed to submit late proposals',
         'pretty_name': 'Late Submitter', 'display_order': None,
         'name': 'late_submitter'},
        {'comment': 'Has access to the funding review system',
         'pretty_name': 'Funding Reviewer', 'display_order': None,
         'name': 'funding_reviewer'},
        {
            'comment':
                'Members of the press and media who can receive a press ticket',
            'pretty_name': 'Press Pass', 'display_order': None,
            'name': 'press'},
        {'comment': 'Only gives access to Monday and Tuesday',
         'pretty_name': 'Miniconfs Only', 'display_order': None,
         'name': 'miniconfsonly'}
    ],
    'social_network': [
        {'url': 'http://twitter.com/USER', 'logo': 'tag_twitter.png',
         'name': 'Twitter'},
        {'url': 'http://identi.ca/USER', 'logo': 'tag_identica.png',
         'name': 'Identi.ca'},
        {'url': 'http://www.flickr.com/photos/USER', 'logo': 'tag_flickr.png',
         'name': 'Flickr'}
    ],
    'product_category': [
        {
            'description': (
                'Please choose your registration type. See '
                '<a href="/register/prices" target="_blank">the website</a> '
                'for a description of what is included in each ticket type.'
            ),
            'display_order': 1, 'note': None, 'max_qty': 1,
            'invoice_free_products': True, 'display_mode': None, 'min_qty': 1,
            'display': 'radio', 'name': 'Ticket'},
        {'description': 'Please choose how many t-shirts you would like.',
         'display_order': 10,
         'note': (
             'One t-shirt is free with your registration, and one t-shirt is '
             'free with every adult Partner Programme ticket purchased. Any '
             'additional t-shirts are $25.00 each. More details and '
             'measurements on t-shirt sizes can be found on the '
             '<a href="/register/shirts" target="_blank">registration '
             'information</a>.'),
         'max_qty': 100, 'invoice_free_products': True, 'display_mode': 'shirt',
         'min_qty': 1, 'display': 'qty', 'name': 'T-Shirt'},
        {
            'description': (
                'Please indicate how many Penguin Dinner tickets you would '
                'like.'),
            'display_order': 20,
            'note': (
                "You should include yourself in this number, even if you "
                "register as a Professional. An adult ticket includes an "
                "adult's meal, a child ticket includes a child's meal, and an "
                "infant ticket does not include any meal and the infant will "
                "need to sit on your knee.  If your child requires an adult "
                "meal, then please purchase an adult ticket for them."),
            'max_qty': 5, 'invoice_free_products': True, 'display_mode': 'grid',
            'min_qty': 0, 'display': 'qty', 'name': 'Penguin Dinner Ticket'},
        {
            'description': 'Please indicate how many Speaker Dinner " \
            "tickets you would like.',
            'display_order': 25,
            'note': (
                "You should include yourself in this number, even if you "
                "register as a Speaker. These are for you, your significant "
                "other, and your children. An adult ticket includes an "
                "adult's meal, a child ticket includes a child's meal, and "
                "an infant ticket does not include any meal and the infant "
                "will need to sit on your knee. If your child requires an "
                "adult meal, then select an adult ticket for them."),
            'max_qty': 200, 'invoice_free_products': True,
            'display_mode': 'grid', 'min_qty': 0, 'display': 'qty',
            'name': 'Speakers Dinner Ticket'},
        {
            'description': 'Please consider where you are going to stay " \
            "during the conference.',
            'display_order': 30, 'note': None, 'max_qty': 10,
            'invoice_free_products': False, 'display_mode': None, 'min_qty': 0,
            'display': 'select', 'name': 'Accommodation'},
        {
            'description': 'Please indicate interest for your partner and " \
            "children to attend the Partners Programme.',
            'display_order': 40,
            'note': (
                'This does NOT indicate your attendance and there will be an '
                'additional cost if your partner attends the programme. We '
                'will contact you shortly regarding the cost and details of '
                'the programme.'),
            'max_qty': 50, 'invoice_free_products': True,
            'display_mode': 'grid', 'min_qty': 0, 'display': 'qty',
            'name': "Partners' Programme"},
        {
            'description': (
                'Please indicate your preferences for the miniconfs that '
                'will be running on Monday and Tuesday. Check the '
                '<a href="/programme/miniconfs" target="_blank">Miniconfs '
                'page</a> for details on each event. You can choose to '
                'attend multiple miniconfs in the one day, as the schedules '
                'will be published ahead of the conference for you to swap '
                'sessions.'),
            'display_order': 100,
            'note': (
                'The Rocketry Miniconf is the only paid miniconf and seats '
                'are limited, it would be expected that you would attend for '
                'the entire day. If you have not added this ticket to your '
                'registration and paid, you will not be able to attend. The '
                'cost covers supplies, travel to the launch site, insurance '
                'and a one-day Rocketry Club membership.'),
            'max_qty': 50, 'invoice_free_products': False,
            'display_mode': 'miniconf', 'min_qty': 0, 'display': 'checkbox',
            'name': 'Miniconfs'}
        ],
    'ceiling': [
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'conference-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'conference-paid', 'max_sold': 750},
        {'parent_id': None, 'available_from': None,
         'available_until': datetime.datetime(2010, 10, 28, 23, 59, 59),
         'name': 'conference-earlybird', 'max_sold': 200},
        {'parent_id': None,
         'available_from': datetime.datetime(2010, 10, 29, 0, 0),
         'available_until': None, 'name': 'conference-non-earlybird',
         'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'shirt-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'shirt-men', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'shirt-women', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'penguindinner-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'speakersdinner-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'accomodation-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'partners-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'miniconf-all', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'miniconf-monday', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'miniconf-tuesday', 'max_sold': None},
        {'parent_id': None, 'available_from': None, 'available_until': None,
         'name': 'miniconf-rocketry', 'max_sold': 24}],

    'person': [
        {'activated': True, 'postcode': None,
         'email_address': 'admin@zookeepr.org',
         'password_hash':
             '4429e49e23f64a1d068fe8a7031fd0c2a04b71804b86a7d7d5c16b1547d102b1',
         'city': None,
         'url_hash':
             '3fc816acb06e87f573a6efbbac0115c64251fb952eb89fce734afcf4e3c73199',
         'password_salt':
             '8b3d140adec9ad3599e4bba91fb99849cd7d03a7009f71cebb02f64984b6cf48',
         'state': None, 'lastname': 'User', 'i_agree': False,
         'creation_timestamp': datetime.datetime(2015, 8, 4, 10, 57, 30,
                                                 823206), 'address2': None,
         'bio': None, 'firstname': 'Admin', 'address1': None, 'company': None,
         'phone': None, 'badge_printed': False, 'mobile': None, 'country': None,
         'experience': None, 'url': None,
         'last_modification_timestamp': datetime.datetime.now()
         }],

    'person_role_map': [{'person_id': 1, 'role_id': 1}],
    'product': [
        {'cost': '12500', 'description': 'Student Ticket', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 1},
        {'cost': '29900', 'description': 'Earlybird Hobbyist Ticket',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '37500', 'description': 'Hobbyist Ticket', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 1},
        {'cost': '63500', 'description': 'Earlybird Professional Ticket',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '79500', 'description': 'Professional Ticket',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '150000', 'description': 'Fairy Penguin Sponsor',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '0', 'description': 'Speaker Ticket', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': 'self.is_speaker()',
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '0', 'description': 'Miniconf Organiser Ticket',
         'display_order': 10, 'fulfilment_type_id': None,
         'auth': 'self.is_miniconf_org()', 'badge_text': None, 'active': True,
         'validate': None, 'category_id': 1},
        {'cost': '0', 'description': 'Volunteer Ticket (Free)',
         'display_order': 10, 'fulfilment_type_id': None,
         'auth': 'self.is_volunteer(product)', 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 1},
        {'cost': '12500', 'description': 'Volunteer Ticket (paid)',
         'display_order': 10, 'fulfilment_type_id': None,
         'auth': 'self.is_volunteer(product)', 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 1},
        {'cost': '0', 'description': 'Press Ticket', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': "self.is_role('press')",
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '0', 'description': 'Team Ticket', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': "self.is_role('team')",
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 1},
        {'cost': '0', 'description': 'Monday Southern Plumbers',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Monday Haecksen', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 7},
        {'cost': '0', 'description': 'Monday Multimedia + Music',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Monday Arduino', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 7},
        {'cost': '0', 'description': 'Monday Open Programming',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Monday The Business of Open Source',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Monday Freedom in the cloud',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Multicore and Parallel Computing',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '20000', 'description': 'Tuesday Rocketry',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Systems Administration',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Open in the public sector ',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Mobile FOSS', 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Data Storage',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Research and Student Innovation',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '0', 'description': 'Tuesday Libre Graphics Day',
         'display_order': 10, 'fulfilment_type_id': None, 'auth': None,
         'badge_text': None, 'active': True, 'validate': None,
         'category_id': 7},
        {'cost': '2500', 'description': "Men's Small", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's Medium", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's Large", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's XL", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's 2XL", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's 3XL", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's 5XL", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Men's 7XL", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 6", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 8", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 10", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 12", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 14", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 16", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 18", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 20", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {'cost': '2500', 'description': "Women's Size 22", 'display_order': 10,
         'fulfilment_type_id': None, 'auth': None, 'badge_text': None,
         'active': True, 'validate': None, 'category_id': 2},
        {
            'cost': '9000',
            'description': 'Adult',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None,
            'badge_text': None,
            'active': True,
            'validate': (
                "ProDinner(dinner_field='product_Penguin Dinner "
                "Ticket_Adult_qty',ticket_category='category_Ticket',"
                "ticket_id=[4,5,6,7,8,11,12])"
            ),
            'category_id': 3
        },
        {
            'cost': '2000',
            'description': 'Child',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None,
            'badge_text': None,
            'active': True, 'validate': None,
            'category_id': 3
        },
        {
            'cost': '0',
            'description': 'Infant',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None, 'badge_text': None,
            'active': True, 'validate': None,
            'category_id': 3
        },
        {
            'cost': '0', 'description': 'Adult', 'display_order': 10,
            'fulfilment_type_id': None,
            'auth':
                "self.is_speaker() or self.is_miniconf_org() or "
                "self.is_role('team')",
            'badge_text': None, 'active': True,
            'validate':
                "ProDinner(dinner_field='product_Speakers Dinner "
                "Ticket_Adult_qty',ticket_category='category_Ticket',"
                "ticket_id=[7,8,12])",
            'category_id': 4
        },
        {
            'cost': '0',
            'description': 'Child',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth':
                "self.is_speaker() or self.is_miniconf_org() or "
                "self.is_role('team')",
            'badge_text': None,
            'active': True,
            'validate': None,
            'category_id': 4
        },
        {
            'cost': '0',
            'description': 'Infant',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth':
                "self.is_speaker() or self.is_miniconf_org() or "
                "self.is_role('team')",
            'badge_text': None,
            'active': True,
            'validate': None,
            'category_id': 4
        },
        {
            'cost': '0',
            'description': 'I will organise my own',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None,
            'badge_text': None,
            'active': True,
            'validate': None,
            'category_id': 5
        },
        {
            'cost': '23500',
            'description': 'Adult',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None,
            'badge_text': None,
            'active': True,
            'validate':
                "PPDetails(adult_field='product_Partners "
                "Programme_Adult_qty', email_field='partner_email', "
                "name_field='partner_name', mobile_field='partner_mobile')",
            'category_id': 6
        },
        {
            'cost': '16500',
            'description': 'Child (3-14 years old)',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None,
            'badge_text': None,
            'active': True,
            'validate':
                "PPChildrenAdult(current_field='product_Partners "
                "Programme_Child (3_14 years old)_qty',adult_field="
                "'product_Partners Programme_Adult_qty')",
            'category_id': 6
        },
        {
            'cost': '0',
            'description': 'Infant (0-2 years old)',
            'display_order': 10,
            'fulfilment_type_id': None,
            'auth': None,
            'badge_text': None,
            'active': True,
            'validate':
                "PPChildrenAdult(current_field='product_Partners "
                "Programme_Child (0_2 years old)_qty',adult_field="
                "'product_Partners Programme_Adult_qty')",
            'category_id': 6
        }
    ],
    'product_ceiling_map': [
        {'product_id': 5, 'ceiling_id': 2},
        {'product_id': 5, 'ceiling_id': 1},
        {'product_id': 5, 'ceiling_id': 4},
        {'product_id': 10, 'ceiling_id': 1},
        {'product_id': 1, 'ceiling_id': 2},
        {'product_id': 1, 'ceiling_id': 1},
        {'product_id': 3, 'ceiling_id': 2},
        {'product_id': 3, 'ceiling_id': 1},
        {'product_id': 3, 'ceiling_id': 4},
        {'product_id': 9, 'ceiling_id': 1},
        {'product_id': 8, 'ceiling_id': 1},
        {'product_id': 6, 'ceiling_id': 2},
        {'product_id': 6, 'ceiling_id': 1},
        {'product_id': 2, 'ceiling_id': 2},
        {'product_id': 2, 'ceiling_id': 1},
        {'product_id': 2, 'ceiling_id': 3},
        {'product_id': 11, 'ceiling_id': 1},
        {'product_id': 4, 'ceiling_id': 2},
        {'product_id': 4, 'ceiling_id': 1},
        {'product_id': 4, 'ceiling_id': 3},
        {'product_id': 7, 'ceiling_id': 1},
        {'product_id': 23, 'ceiling_id': 12},
        {'product_id': 23, 'ceiling_id': 14},
        {'product_id': 22, 'ceiling_id': 12},
        {'product_id': 22, 'ceiling_id': 14},
        {'product_id': 17, 'ceiling_id': 12},
        {'product_id': 17, 'ceiling_id': 13},
        {'product_id': 24, 'ceiling_id': 12},
        {'product_id': 24, 'ceiling_id': 14},
        {'product_id': 26, 'ceiling_id': 12},
        {'product_id': 26, 'ceiling_id': 14},
        {'product_id': 15, 'ceiling_id': 12},
        {'product_id': 15, 'ceiling_id': 13},
        {'product_id': 25, 'ceiling_id': 12},
        {'product_id': 25, 'ceiling_id': 14},
        {'product_id': 18, 'ceiling_id': 12},
        {'product_id': 18, 'ceiling_id': 13},
        {'product_id': 14, 'ceiling_id': 12},
        {'product_id': 14, 'ceiling_id': 13},
        {'product_id': 13, 'ceiling_id': 12},
        {'product_id': 13, 'ceiling_id': 13},
        {'product_id': 20, 'ceiling_id': 12},
        {'product_id': 20, 'ceiling_id': 14},
        {'product_id': 16, 'ceiling_id': 12},
        {'product_id': 16, 'ceiling_id': 13},
        {'product_id': 19, 'ceiling_id': 12},
        {'product_id': 19, 'ceiling_id': 13},
        {'product_id': 21, 'ceiling_id': 12},
        {'product_id': 21, 'ceiling_id': 14},
        {'product_id': 21, 'ceiling_id': 15},
        {'product_id': 27, 'ceiling_id': 12},
        {'product_id': 27, 'ceiling_id': 13},
        {'product_id': 41, 'ceiling_id': 5},
        {'product_id': 41, 'ceiling_id': 7},
        {'product_id': 35, 'ceiling_id': 5},
        {'product_id': 35, 'ceiling_id': 6},
        {'product_id': 34, 'ceiling_id': 5},
        {'product_id': 34, 'ceiling_id': 6},
        {'product_id': 31, 'ceiling_id': 5},
        {'product_id': 31, 'ceiling_id': 6},
        {'product_id': 33, 'ceiling_id': 5},
        {'product_id': 33, 'ceiling_id': 6},
        {'product_id': 32, 'ceiling_id': 5},
        {'product_id': 32, 'ceiling_id': 6},
        {'product_id': 28, 'ceiling_id': 5},
        {'product_id': 28, 'ceiling_id': 6},
        {'product_id': 37, 'ceiling_id': 5},
        {'product_id': 37, 'ceiling_id': 7},
        {'product_id': 44, 'ceiling_id': 5},
        {'product_id': 44, 'ceiling_id': 7},
        {'product_id': 38, 'ceiling_id': 5},
        {'product_id': 38, 'ceiling_id': 7},
        {'product_id': 36, 'ceiling_id': 5},
        {'product_id': 36, 'ceiling_id': 7},
        {'product_id': 39, 'ceiling_id': 5},
        {'product_id': 39, 'ceiling_id': 7},
        {'product_id': 43, 'ceiling_id': 5},
        {'product_id': 43, 'ceiling_id': 7},
        {'product_id': 29, 'ceiling_id': 5},
        {'product_id': 29, 'ceiling_id': 6},
        {'product_id': 40, 'ceiling_id': 5},
        {'product_id': 40, 'ceiling_id': 7},
        {'product_id': 42, 'ceiling_id': 5},
        {'product_id': 42, 'ceiling_id': 7},
        {'product_id': 30, 'ceiling_id': 5},
        {'product_id': 30, 'ceiling_id': 6},
        {'product_id': 45, 'ceiling_id': 8},
        {'product_id': 46, 'ceiling_id': 8},
        {'product_id': 49, 'ceiling_id': 9},
        {'product_id': 48, 'ceiling_id': 9},
        {'product_id': 51, 'ceiling_id': 10},
        {'product_id': 53, 'ceiling_id': 11},
        {'product_id': 52, 'ceiling_id': 11},
        {'product_id': 54, 'ceiling_id': 11},
    ],
    'accommodation_assistance_type': [
        {'name': 'I do not require accommodation assistance.'},
        {
            'name':
                'I request that linux.conf.au provide student-style '
                'single room accommodation for the duration of the conference.'
        }
    ],
    'target_audience': [
        {'name': 'Community'},
        {'name': 'User'},
        {'name': 'Developer'},
        {'name': 'Business'}
    ],
    'proposal_type': [
        {'name': 'Presentation', 'notify_email': None},
        {'name': 'Miniconf', 'notify_email': None},
        {'name': 'Tutorial - 1 hour and 45 minutes', 'notify_email': None},
        {'name': 'Tutorial - 3 hours and 30 minutes', 'notify_email': None},
        {'name': 'Poster', 'notify_email': None}
    ],
    'funding_type': [
        {
            'active': True,
            'note':
                'Assists people from diverse groups, including females in IT '
                'and disabled people',
            'name': 'Google Diversity Programme',
            'notify_email': None
        }
    ],
    'travel_assistance_type': [
        {'name': 'I do not require travel assistance.'},
        {'name': 'I request that linux.conf.au book and pay for air travel.'},
    ],
    'db_content_type': [
        {'name': 'Page'},
        {'name': 'News'},
        {'name': 'In the press'},
        {'name': 'Redirect'},
    ],

    'special_offer':
        [{
         'id_name': 'LA member number',
         'enabled': False,
         'description':
             '<p>Welcome to Linux Australia members!</p><p>We are happy to '
             'invite you to register for LCA before we open registrations '
             'to the general public. To take advantage of this special '
             'offer, simply enter your LA member number (which you can see '
             'on your '
             '<a href="https://www.linux.org.au/membership/index.php?page='
             'edit-member">details page</a> once you are logged in).</p>',
         'name': 'LinuxAustralia'
         }],

    'funding_status': [
        {'name': 'Accepted'},
        {'name': 'Declined'},
        {'name': 'Pending'},
        {'name': 'Withdrawn'}
    ],

    'proposal_status': [
        {'name': 'Accepted'},
        {'name': 'Declined'},
        {'name': 'Pending Review'},
        {'name': 'Withdrawn'},
        {'name': 'Backup'},
        {'name': 'Offered'},
        {'name': 'Offered Travel'},
        {'name': 'Offered Accommodation'},
        {'name': 'Offered Travel Accommodation'},
        {'name': 'Contact'},
    ],

    'product_include': [
        {'product_id': 1, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 2, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 3, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 4, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 5, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 6, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 7, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 8, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 9, 'include_category_id': 2, 'include_qty': 2},
        {'product_id': 10, 'include_category_id': 2, 'include_qty': 2},
        {'product_id': 11, 'include_category_id': 2, 'include_qty': 1},
        {'product_id': 12, 'include_category_id': 2, 'include_qty': 6},
        {'product_id': 4, 'include_category_id': 3, 'include_qty': 1},
        {'product_id': 5, 'include_category_id': 3, 'include_qty': 1},
        {'product_id': 6, 'include_category_id': 3, 'include_qty': 1},
        {'product_id': 7, 'include_category_id': 3, 'include_qty': 1},
        {'product_id': 8, 'include_category_id': 3, 'include_qty': 1},
        {'product_id': 11, 'include_category_id': 3, 'include_qty': 1},
        {'product_id': 12, 'include_category_id': 3, 'include_qty': 2},
        {'product_id': 7, 'include_category_id': 6, 'include_qty': 2},
    ]
}


def insert_rows(connection, table_name):
    log.info('Loading data for {0}'.format(table_name))
    table = sa.schema.Table(
        table_name, meta, autoload=True, autoload_with=connection)
    connection.execute(table.insert().values(data[table_name]))


def delete_rows(connection, table_name):
    log.info('Deleting data from {0}'.format(table_name))
    table = sa.schema.Table(
        table_name, meta, autoload=True, autoload_with=connection)
    connection.execute(table.delete())


def upgrade():
    connection = op.get_bind()
    people = sa.schema.Table(
        'person', meta, autoload=True, autoload_with=connection)
    people_count = connection.execute(people.count()).first()[0]
    log.info('Checking for existing data in the database')
    if people_count:
        raise sa.exc.SQLAlchemyError(
            'Data has already been loaded into this database'
        )

    for table in tables:
        insert_rows(connection, table)


def downgrade():
    connection = op.get_bind()

    for table in tables_delete_order:
        delete_rows(connection, table)