"""empty message

Revision ID: 2daf319bbf1
Revises: None
Create Date: 2012-06-10 11:22:51.540533

"""

# revision identifiers, used by Alembic.
revision = '2daf319bbf1'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
metadata=MetaData()
Base = declarative_base(metadata=metadata)


def upgrade():
    def add_proposals(session):        

        class ProposalStatus(Base):
            __tablename__ = 'proposal_status'
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.String(40), unique=True, nullable=False)
        
        class ProposalType(Base):
            __tablename__ = 'proposal_type'
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.String(40), unique=True, nullable=False)
        
        class TravelAssistanceType(Base):
            __tablename__ = 'travel_assistance_type'
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.String(60), unique=True, nullable=False)
        
        class TargetAudience(Base):
            __tablename__ = 'target_audience'

            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.String(40), unique=True, nullable=False)
        
        class AccommodationAssistanceType(Base):
            __tablename__ = 'accommodation_assistance_type'

            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.String(120), unique=True, nullable=False)
        
        session.add_all(
            [
                ProposalStatus(name='Accepted'),
                ProposalStatus(name='Rejected'),
                ProposalStatus(name='Pending'),
                ProposalStatus(name='Withdrawn'),
                ProposalStatus(name='Backup'),
            ]
        )
        session.add_all(
            [
                ProposalType(name='Presentation'),
                ProposalType(name='Miniconf'),
                ProposalType(name='Tutorial - 1 hour and 45 minutes'),
                ProposalType(name='Tutorial - 3 hours and 30 minutes'),
                ProposalType(name='Poster'),
            ]
        )
        session.add_all(
            [
                TravelAssistanceType(name='I do not require travel assistance.'),
                TravelAssistanceType(name='I request that linux.conf.au book and pay for air travel.'),
            ]
        )
        session.add_all(
            [
                TargetAudience(name='Community'),
                TargetAudience(name='User'),
                TargetAudience(name='Developer'),
                TargetAudience(name='Business'),
            ]
        )
        session.add_all(
            [
                AccommodationAssistanceType(name='I do not require accommodation assistance.'),
                AccommodationAssistanceType(name='I request that linux.conf.au provide student-style single room accommodation for the duration of the conference.'),
            ]
        )

    def add_db_content_types(setup):
        class DbContentType(Base):
            __tablename__ = 'db_content_type'

            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.Text, nullable=False, unique=True)
            
        session.add_all(
            [
                DbContentType(name='Page'),
                DbContentType(name='News'),
                DbContentType(name='In the press'),
                DbContentType(name='Redirect'),
            ]
        )

    def add_funding(session):
        
        class FundingStatus(Base):
            __tablename__ = 'funding_status'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.String(40), unique=True, nullable=False)


        class FundingType(Base):
            __tablename__ = 'funding_type'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            active = sa.Column(sa.types.Boolean, nullable=False)
            name = sa.Column(sa.types.String(40), unique=True, nullable=False)
            note = sa.Column(sa.types.String())

        session.add_all(
             [
                 FundingStatus(name='Accepted'),
                 FundingStatus(name='Declined'),
                 FundingStatus(name='Pending'),
                 FundingStatus(name='Withdrawn'),
             ]
        )
        session.add_all(
             [
                 FundingType(name='Google Diversity Programme',
                   note='Assists people from diverse groups, including females in IT and disabled people', active=True),
             ]
         )

    def add_special_offers(session):
        class SpecialRegistration(Base):
            """Stores details of a person who used a special offer to register early
            """
            __tablename__ = 'special_registration'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            member_number = sa.Column(sa.types.Text, nullable=True, unique=False)
            special_offer_id = sa.Column(sa.types.Integer, sa.ForeignKey('special_offer.id'), nullable=False)
            person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)

        class SpecialOffer(Base):
            """Stores details about a special offer for pre-registration
            """
            __tablename__ = 'special_offer'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            enabled = sa.Column(sa.types.Boolean, nullable=False)
            name = sa.Column(sa.types.Text, nullable=False, unique=True)
            description = sa.Column(sa.types.Text, nullable=False)
            id_name = sa.Column(sa.types.Text)
        
            special_registrations = sa.orm.relation(SpecialRegistration, backref='special_offer')
        
        session.add_all(
            [
                SpecialOffer(
                    name='LinuxAustralia', 
                    description='<p>Welcome to Linux Australia members!</p>'
                    '<p>We are happy to invite you to register for LCA before'
                    ' we open registrations to the general public. To take '
                    'advantage of this special offer, simply enter your LA '
                    'member number (which you can see on your '
                    '<a href="https://www.linux.org.au/membership/index.'
                    'php?page=edit-member">details page</a> once you are '
                    'logged in).</p>', 
                    id_name='LA member number', 
                    enabled=False
                    ),
            ]
        )
    def add_ceilings(session):
        import datetime
        from zk.model.ceiling import Ceiling
        
        # Ceiling 
        earlybird_end = datetime.datetime(2010, 10, 28, 23, 59, 59);
        nonearlybird_start = datetime.datetime(2010, 10, 29, 0, 0, 0,);
    
        session.add_all(
            [
                Ceiling(name='conference-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='conference-paid', max_sold=750, available_from=None, available_until=None),
                Ceiling(name='conference-earlybird', max_sold=200, available_from=None, available_until=earlybird_end),
                Ceiling(name='conference-non-earlybird', max_sold=None, available_from=nonearlybird_start, available_until=None),
                Ceiling(name='shirt-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='shirt-men', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='shirt-women', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='penguindinner-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='speakersdinner-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='accomodation-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='partners-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='miniconf-all', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='miniconf-monday', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='miniconf-tuesday', max_sold=None, available_from=None, available_until=None),
                Ceiling(name='miniconf-rocketry', max_sold=24, available_from=None, available_until=None),
            ]
        )

    def add_roles(session):
        from zk.model.role import Role
        for r in [
              Role(name='organiser', pretty_name='Organizer', comment='Has full access to management pages'),
              Role(name='team', pretty_name='Core Team', comment='Member of core team'),
              Role(name='reviewer', pretty_name='Paper Reviewer', comment='Has access to the paper review system'),
              Role(name='miniconf', pretty_name='Miniconf Organiser', comment='Is a miniconference organiser'),
              Role(name='papers_chair', pretty_name='Papers Chair', comment='Has access to paper review system management functions'),
              Role(name='late_submitter', pretty_name='Late Submitter', comment='Is allowed to submit paper proposals late'),
              Role(name='funding_reviewer', pretty_name='Funding Reviewer', comment='Has access to the funding review system'),
              Role(name='press', pretty_name='Press Pass', comment='Members of the press and media who can receive a press ticket'),
              Role(name='miniconfsonly', pretty_name='Miniconfs Only', comment='Only gives access to Monday and Tuesday')
          ]:
            session.add(r)
        
    def add_people(session):
        import random, hashlib
        class Role(Base):
            __tablename__ = 'role'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.Text, unique=True, nullable=False)
            pretty_name = sa.Column(sa.types.Text, nullable=True)
            display_order = sa.Column(sa.types.Integer, nullable=True)
            comment = sa.Column(sa.types.Text, nullable=True)
        

        person_role_map = sa.Table(
            'person_role_map', 
            metadata,
            sa.Column(
                'person_id', 
                sa.types.Integer, 
                sa.ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE'), 
                primary_key=True, nullable=False),
            sa.Column(
                'role_id',   sa.types.Integer, 
                sa.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), 
                primary_key=True, nullable=False)
        )
        
        class Person(Base):
            __tablename__ = 'person'        
            id = sa.Column(sa.types.Integer, primary_key=True)
            email_address = sa.Column(sa.types.Text, nullable=False, unique=True)
            password_hash = sa.Column(sa.types.Text)
            creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
            last_modification_timestamp = sa.Column(
                sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())
            url_hash = sa.Column(sa.types.String(32), nullable=False, index=True)
            activated = sa.Column(sa.types.Boolean, nullable=False, default=False)
            firstname = sa.Column(sa.types.Text)
            lastname = sa.Column(sa.types.Text)
            address1 = sa.Column(sa.types.Text)
            address2 = sa.Column(sa.types.Text)
            city = sa.Column(sa.types.Text)
            state = sa.Column(sa.types.Text)
            postcode = sa.Column(sa.types.Text)
            country = sa.Column(sa.types.Text)
            company = sa.Column(sa.types.Text)
            phone = sa.Column(sa.types.Text)
            mobile = sa.Column(sa.types.Text)
            url = sa.Column(sa.types.Text)
            experience = sa.Column(sa.types.Text)
            bio = sa.Column(sa.types.Text)        
            i_agree = sa.Column(sa.types.Boolean, nullable=False, default=False)
            badge_printed = sa.Column(sa.types.Boolean, default='False')
            roles = sa.orm.relation(Role, secondary=person_role_map, backref='people', order_by=Role.name)

            def gen_password(self, value):
                m = hashlib.md5()
                m.update(value)
                return m.hexdigest()
            
            def _set_password(self, value):
                if value is not None:
                    self.password_hash = self.gen_password(value)

            def _get_password(self):
                return self.password_hash
        
            password = property(_get_password, _set_password)
        
            def _update_url_hash(self):
                """Update the stored URL hash for this person.
        
                Call this when an element of the URL hash has changed
                (i.e. either the email address or timestamp)
                """
                nonce = random.randrange(0, 2**30)
                magic = "%s&%s&%s" % (self.email_address,
                                      self.creation_timestamp,
                                      nonce)
                self.url_hash = self.gen_password(magic)
            
            
            
            
        person = Person(
            email_address="admin@zk.org",
            activated=True,
            firstname="Admin",
            lastname="User"
        )
        person.password = 'password'
        person.activated = True
        person._update_url_hash()
    
        # Cannot just use the find_by_name function because it assumes a global called Session
        role = session.query(Role).filter_by(name='organiser').one()
        person.roles.append(role)
    
        session.add(person)
        
    def add_products(session):
        from zk.model.ceiling import Ceiling
        from zk.model.product_category import ProductCategory
        from zk.model.product import Product, ProductInclude
        
        def product_category_by_name(name):
            return session.query(ProductCategory).filter_by(name=name).first()
        
        def ceiling_by_name(name):
            return session.query(Ceiling).filter_by(name=name).first()
        
        # Product
        category_ticket = product_category_by_name('Ticket')
    
        ceiling_conference = ceiling_by_name('conference-paid')
        ceiling_all_conference = ceiling_by_name('conference-all')
        ceiling_earlybird = ceiling_by_name('conference-earlybird')
        ceiling_nonearlybird = ceiling_by_name('conference-non-earlybird')
    
        # Tickets
        ticket_student = Product(category=category_ticket, active=True, description="Student Ticket",
                          cost="12500", auth=None, validate=None)
        ticket_student.ceilings.append(ceiling_conference)
        ticket_student.ceilings.append(ceiling_all_conference)
        session.add(ticket_student);
    
        ticket_hobbyist_eb = Product(category=category_ticket, active=True, description="Earlybird Hobbyist Ticket",
                          cost="29900", auth=None, validate=None)
        ticket_hobbyist_eb.ceilings.append(ceiling_conference)
        ticket_hobbyist_eb.ceilings.append(ceiling_all_conference)
        ticket_hobbyist_eb.ceilings.append(ceiling_earlybird)
        session.add(ticket_hobbyist_eb);
    
        ticket_hobbyist = Product(category=category_ticket, active=True, description="Hobbyist Ticket",
                          cost="37500", auth=None, validate=None)
        ticket_hobbyist.ceilings.append(ceiling_conference)
        ticket_hobbyist.ceilings.append(ceiling_all_conference)
        ticket_hobbyist.ceilings.append(ceiling_nonearlybird)
        session.add(ticket_hobbyist);
    
        ticket_professional_eb = Product(category=category_ticket, active=True, description="Earlybird Professional Ticket",
                          cost="63500", auth=None, validate=None)
        ticket_professional_eb.ceilings.append(ceiling_conference)
        ticket_professional_eb.ceilings.append(ceiling_all_conference)
        ticket_professional_eb.ceilings.append(ceiling_earlybird)
        session.add(ticket_professional_eb);
    
        ticket_professional = Product(category=category_ticket, active=True, description="Professional Ticket",
                          cost="79500", auth=None, validate=None)
        ticket_professional.ceilings.append(ceiling_conference)
        ticket_professional.ceilings.append(ceiling_all_conference)
        ticket_professional.ceilings.append(ceiling_nonearlybird)
        session.add(ticket_professional);
    
        ticket_fairy_penguin = Product(category=category_ticket, active=True, description="Fairy Penguin Sponsor",
                          cost="150000", auth=None, validate=None)
        ticket_fairy_penguin.ceilings.append(ceiling_conference)
        ticket_fairy_penguin.ceilings.append(ceiling_all_conference)
        session.add(ticket_fairy_penguin);
    
        ticket_speaker = Product(category=category_ticket, active=True, description="Speaker Ticket",
                          cost="0", auth="self.is_speaker()", validate=None)
        ticket_speaker.ceilings.append(ceiling_all_conference)
        session.add(ticket_speaker);
    
        ticket_miniconf = Product(category=category_ticket, active=True, description="Miniconf Organiser Ticket",
                          cost="0", auth="self.is_miniconf_org()", validate=None)
        ticket_miniconf.ceilings.append(ceiling_all_conference)
        session.add(ticket_miniconf);
    
        ticket_volunteer_free = Product(category=category_ticket, active=True, description="Volunteer Ticket (Free)",
                          cost="0", auth="self.is_volunteer(product)", validate=None)
        ticket_volunteer_free.ceilings.append(ceiling_all_conference)
        session.add(ticket_volunteer_free);
    
        ticket_volunteer_paid = Product(category=category_ticket, active=True, description="Volunteer Ticket (paid)",
                          cost="12500", auth="self.is_volunteer(product)", validate=None)
        ticket_volunteer_paid.ceilings.append(ceiling_all_conference)
        session.add(ticket_volunteer_paid);
    
        ticket_press = Product(category=category_ticket, active=True, description="Press Ticket",
                          cost="0", auth="self.is_role('press')", validate=None)
        ticket_press.ceilings.append(ceiling_all_conference)
        session.add(ticket_press)
    
        ticket_team = Product(category=category_ticket, active=True, description="Team Ticket",
                          cost="0", auth="self.is_role('team')", validate=None)
    
        # Miniconfs
        category_miniconf = product_category_by_name('Miniconfs')
    
        ceiling_miniconf_all = ceiling_by_name('miniconf-all')
        ceiling_miniconf_monday = ceiling_by_name('miniconf-monday')
        ceiling_miniconf_tuesday = ceiling_by_name('miniconf-tuesday')
        ceiling_rocketry = ceiling_by_name('miniconf-rocketry')
    
        product = Product(category=category_miniconf, active=True, description="Monday Southern Plumbers",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Monday Haecksen",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Monday Multimedia + Music",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Monday Arduino",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Monday Open Programming",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Monday The Business of Open Source",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Monday Freedom in the cloud",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Multicore and Parallel Computing",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Rocketry",
                          cost="20000", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        product.ceilings.append(ceiling_rocketry)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Systems Administration",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Open in the public sector ",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Mobile FOSS",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Data Storage",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Research and Student Innovation",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_tuesday)
        session.add(product)
    
        product = Product(category=category_miniconf, active=True, description="Tuesday Libre Graphics Day",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_miniconf_all)
        product.ceilings.append(ceiling_miniconf_monday)
        session.add(product)
    
        # Shirts
        category_shirt = product_category_by_name('T-Shirt')
    
        ceiling_shirt_all = ceiling_by_name('shirt-all')
        ceiling_shirt_men = ceiling_by_name('shirt-men')
        ceiling_shirt_women = ceiling_by_name('shirt-women')
    
        product = Product(category=category_shirt, active=True, description="Men's Small", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Men's Medium", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
    
        product = Product(category=category_shirt, active=True, description="Men's Large", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Men's XL", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Men's 2XL", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Men's 3XL", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Men's 5XL", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Men's 7XL", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_men)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 6", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 8", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 10", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 12", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 14", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 16", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 18", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 20", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        product = Product(category=category_shirt, active=True, description="Women's Size 22", cost="2500", auth=None, validate=None)
        product.ceilings.append(ceiling_shirt_all)
        product.ceilings.append(ceiling_shirt_women)
        session.add(product)
    
        # Penguin Dinner
        category_penguin = product_category_by_name('Penguin Dinner Ticket')
    
        ceiling_penguin_all = ceiling_by_name('penguindinner-all')
    
        product = Product(category=category_penguin, active=True, description="Adult", cost="9000", auth=None, validate="ProDinner(dinner_field='product_Penguin Dinner Ticket_Adult_qty',ticket_category='category_Ticket',ticket_id=[4,5,6,7,8,11,12])")
        product.ceilings.append(ceiling_penguin_all)
        session.add(product)
    
        product = Product(category=category_penguin, active=True, description="Child", cost="2000", auth=None, validate=None)
        product.ceilings.append(ceiling_penguin_all)
        session.add(product)
    
        Product(category=category_penguin, active=True, description="Infant", cost="0", auth=None, validate=None)
        session.add(product)
    
        # Speakers Dinner
        category_speakers = product_category_by_name('Speakers Dinner Ticket')
    
        ceiling_speakers_all = ceiling_by_name('speakersdinner-all')
    
        product = Product(category=category_speakers, active=True, description="Adult", cost="0", validate="ProDinner(dinner_field='product_Speakers Dinner Ticket_Adult_qty',ticket_category='category_Ticket',ticket_id=[7,8,12])", auth="self.is_speaker() or self.is_miniconf_org() or self.is_role('team')")
        product.ceilings.append(ceiling_speakers_all)
        session.add(product)
    
        product = Product(category=category_speakers, active=True, description="Child", cost="0", validate=None , auth="self.is_speaker() or self.is_miniconf_org() or self.is_role('team')")
        product.ceilings.append(ceiling_speakers_all)
        session.add(product)
    
        product = Product(category=category_speakers, active=True, description="Infant", cost="0", validate=None , auth="self.is_speaker() or self.is_miniconf_org() or self.is_role('team')")
        session.add(product)
    
        # Accommodation
        category_accomodation = product_category_by_name('Accommodation')
        ceiling_accom_all = ceiling_by_name('accomodation-all')
        ceiling_accom_selfbook = ceiling_by_name('accom1odation-selfbook')
        product = Product(category=category_accomodation, active=True, description="I will organise my own",
                          cost="0", auth=None, validate=None)
        product.ceilings.append(ceiling_accom_all)
        product.ceilings.append(ceiling_accom_selfbook)
        session.add(product);
    
        # Partner's Programme
        category_partners = product_category_by_name('Partners Programme')
        ceiling_partners_all = ceiling_by_name('partners-all')
    
        partners_adult = Product(category=category_partners, active=True, description="Adult", cost="23500", auth=None, validate="PPDetails(adult_field='product_Partners Programme_Adult_qty', email_field='partner_email', name_field='partner_name', mobile_field='partner_mobile')")
        partners_adult.ceilings.append(ceiling_partners_all)
        session.add(partners_adult);
    
        product = Product(category=category_partners, active=True, description="Child (3-14 years old)", cost="16500", auth=None, validate="PPChildrenAdult(current_field='product_Partners Programme_Child (3_14 years old)_qty',adult_field='product_Partners Programme_Adult_qty')")
        product.ceilings.append(ceiling_partners_all)
        session.add(product);
    
        product = Product(category=category_partners, active=True, description="Infant (0-2 years old)", cost="0", auth=None, validate="PPChildrenAdult(current_field='product_Partners Programme_Child (0_2 years old)_qty',adult_field='product_Partners Programme_Adult_qty')")
        product.ceilings.append(ceiling_partners_all)
        session.add(product);
    
        # Product includes
        session.add_all(
            [
                # Include 1 Shirt in all registration types
                ProductInclude(product=ticket_student, include_category=category_shirt, include_qty='1'),           # Student
                ProductInclude(product=ticket_hobbyist_eb, include_category=category_shirt, include_qty='1'),       # Hobbyist EB
                ProductInclude(product=ticket_hobbyist, include_category=category_shirt, include_qty='1'),          # Hobbyist
                ProductInclude(product=ticket_professional_eb, include_category=category_shirt, include_qty='1'),   # Pro EB
                ProductInclude(product=ticket_professional, include_category=category_shirt, include_qty='1'),      # Pro
                ProductInclude(product=ticket_fairy_penguin, include_category=category_shirt, include_qty='1'),     # Fairy
                ProductInclude(product=ticket_speaker, include_category=category_shirt, include_qty='1'),           # Speaker
                ProductInclude(product=ticket_miniconf, include_category=category_shirt, include_qty='1'),          # Miniconf
                ProductInclude(product=ticket_volunteer_free, include_category=category_shirt, include_qty='2'),    # Volunteer
                ProductInclude(product=ticket_volunteer_paid, include_category=category_shirt, include_qty='2'),    # Volunteer
                ProductInclude(product=ticket_press, include_category=category_shirt, include_qty='1'),             # Press
                ProductInclude(product=ticket_team, include_category=category_shirt, include_qty='6'),              # Team
                #ProductInclude(product=partners_adult, include_category=category_shirt, include_qty='1'),           # Partner's Programme get a t-shirt
    
                # Include 1 Dinner for Professional+miniconf and for Speaker registrations
                ProductInclude(product=ticket_professional_eb, include_category=category_penguin, include_qty='1'), # Pro EB
                ProductInclude(product=ticket_professional, include_category=category_penguin, include_qty='1'),    # Pro
                ProductInclude(product=ticket_fairy_penguin, include_category=category_penguin, include_qty='1'),   # Fairy
                ProductInclude(product=ticket_speaker, include_category=category_penguin, include_qty='1'),         # Speaker
                ProductInclude(product=ticket_miniconf, include_category=category_penguin, include_qty='1'),        # Miniconf
                ProductInclude(product=ticket_press, include_category=category_penguin, include_qty='1'),           # Press
                ProductInclude(product=ticket_team, include_category=category_penguin, include_qty='2'),            # Team
    
                # Include 2 partners in the partners program for speakers
                ProductInclude(product=ticket_speaker, include_category=category_partners, include_qty='2'),
            ]
        )
        
    def add_social_media(session):
        class SocialNetwork(Base):
            """Stores the social networks that people might be members of
            """
            __tablename__ = 'social_network'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.Text, unique=True, nullable=False)
            url = sa.Column(sa.types.Text, nullable=False)
            logo = sa.Column(sa.types.Text, nullable=False)
        # Social Media
        session.add_all(
            [
                SocialNetwork(name='Twitter', url='http://twitter.com/USER',
                              logo='tag_twitter.png'),
                SocialNetwork(name='Identi.ca', url='http://identi.ca/USER',
                              logo='tag_identica.png'),
                SocialNetwork(name='Flickr', url='http://www.flickr.com/photos/USER',
                              logo='tag_flickr.png'),
            ]
        )
    
    def add_product_categories(session):        
        class ProductCategory(Base):
            """Stores the product categories used for registration
            """
            __tablename__ = 'product_category'
        
            id = sa.Column(sa.types.Integer, primary_key=True)
            name = sa.Column(sa.types.Text, nullable=False, unique=True)
            description = sa.Column(sa.types.Text, nullable=False)
            note = sa.Column(sa.types.Text)
            display_order = sa.Column(sa.types.Integer, nullable=False)
            display = sa.Column(sa.types.Text, nullable=False) 
            display_mode = sa.Column(sa.types.Text) 
            invoice_free_products = sa.Column(sa.types.Boolean, nullable=False, default=True)        
            min_qty = sa.Column(sa.types.Integer, nullable=True)
            max_qty = sa.Column(sa.types.Integer, nullable=True)
            
        # Product Categories
        session.add_all(
            [
                ProductCategory(
                    name='Ticket', 
                    description='Please choose your registration type. ' +
                    'See <a href="/register/prices" target="_blank">the ' +
                    'website</a> for a description of what is included in ' + 
                    'each ticket type.', 
                    display='radio', min_qty=1, max_qty=1, display_order=1),
                ProductCategory(
                    name='T-Shirt', 
                    description='Please choose how many t-shirts you would '
                    'like.', 
                    note='One t-shirt is free with your registration, and one '
                    't-shirt is free with every adult Partner Programme '
                    'ticket purchased. Any additional t-shirts are $25.00 '
                    'each. More details and measurements on t-shirt sizes '
                    'can be found on the <a href="/register/shirts" '
                    'target="_blank">registration information</a>.', 
                    display='qty', display_mode='shirt', min_qty=1, 
                    max_qty=100, display_order=10),
                ProductCategory(name='Penguin Dinner Ticket', description='Please indicate how many Penguin Dinner tickets you would like.', note='You should include yourself in this number, even if you register as a Professional. An adult ticket includes an adult\'s meal, a child ticket includes a child\'s meal, and an infant ticket does not include any meal and the infant will need to sit on your knee.  If your child requires an adult meal, then please purchase an adult ticket for them.', display='qty', min_qty=0, max_qty=5, display_mode='grid', display_order=20),
                ProductCategory(name='Speakers Dinner Ticket', description='Please indicate how many Speaker Dinner tickets you would like.', note='You should include yourself in this number, even if you register as a Speaker. These are for you, your significant other, and your children. An adult ticket includes an adult\'s meal, a child ticket includes a child\'s meal, and an infant ticket does not include any meal and the infant will need to sit on your knee. If your child requires an adult meal, then select an adult ticket for them.', display='qty', min_qty=0, max_qty=200, display_mode='grid', display_order=25),
                ProductCategory(name='Accommodation', description='Please consider where you are going to stay during the conference.', display='select', invoice_free_products=False, min_qty=0, max_qty=10, display_order=30),
                ProductCategory(name='Partners Programme', description='Please indicate interest for your partner and children to attend the Partners Programme.', note='This does NOT indicate your attendance and there will be an additional cost if your partner attends the programme. We will contact you shortly regarding the cost and details of the programme.', display='qty', min_qty=0, max_qty=50, display_mode='grid', display_order=40),
                ProductCategory(name='Miniconfs', description='Please indicate your preferences for the miniconfs that will be running on Monday and Tuesday. Check the <a href="/programme/miniconfs" target="_blank">Miniconfs page</a> for details on each event. You can choose to attend multiple miniconfs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.', note='The Rocketry Miniconf is the only paid miniconf and seats are limited, it would be expected that you would attend for the entire day. If you have not added this ticket to your registration and paid, you will not be able to attend. The cost covers supplies, travel to the launch site, insurance and a one-day Rocketry Club membership.', display='checkbox', display_mode='miniconf', invoice_free_products=False, min_qty=0, max_qty=50, display_order=100),
            ]
        )

    def create_tables():
        op.create_table('url_hash',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('url_hash', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url'),
        sa.UniqueConstraint('url_hash')
        )
        op.create_table('travel_assistance_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('accommodation_assistance_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('proposal_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('target_audience',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('vote',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rego_id', sa.Integer(), nullable=True),
        sa.Column('vote_value', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('db_content_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('funding_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.Column('note', sa.String(), nullable=True),
        ##sa.CheckConstraint('TODO'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('password_reset_confirmation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email_address', sa.Text(), nullable=False),
        sa.Column('url_hash', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_address'),
        sa.UniqueConstraint('url_hash')
        )
        op.create_table('stream',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('funding_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('special_offer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('id_name', sa.Text(), nullable=True),
        #sa.CheckConstraint('TODO'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('proposal_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('ceiling',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('max_sold', sa.Integer(), nullable=True),
        sa.Column('available_from', sa.DateTime(), nullable=True),
        sa.Column('available_until', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('location',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('display_name', sa.Text(), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('event_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('person',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email_address', sa.Text(), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.Column('url_hash', sa.String(length=32), nullable=False, index=True),
        sa.Column('activated', sa.Boolean(), nullable=False),
        sa.Column('firstname', sa.Text(), nullable=True),
        sa.Column('lastname', sa.Text(), nullable=True),
        sa.Column('address1', sa.Text(), nullable=True),
        sa.Column('address2', sa.Text(), nullable=True),
        sa.Column('city', sa.Text(), nullable=True),
        sa.Column('state', sa.Text(), nullable=True),
        sa.Column('postcode', sa.Text(), nullable=True),
        sa.Column('country', sa.Text(), nullable=True),
        sa.Column('company', sa.Text(), nullable=True),
        sa.Column('phone', sa.Text(), nullable=True),
        sa.Column('mobile', sa.Text(), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('experience', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('badge_printed', sa.Boolean(), nullable=True),
        sa.Column('i_agree', sa.types.Boolean, nullable=False, default=False),
        #sa.CheckConstraint('TODO'),
        #sa.CheckConstraint('TODO'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_address')
        )
        op.create_table('social_network',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('logo', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('product_category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('display', sa.Text(), nullable=False),
        sa.Column('display_mode', sa.Text(), nullable=True),
        sa.Column('invoice_free_products', sa.Boolean(), nullable=False),
        sa.Column('min_qty', sa.Integer(), nullable=True),
        sa.Column('max_qty', sa.Integer(), nullable=True),
        #sa.CheckConstraint('TODO'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('pretty_name', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
        op.create_table('time_slot',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('primary', sa.Boolean(), nullable=False),
        sa.Column('heading', sa.Boolean(), nullable=False),
        sa.CheckConstraint('(start_time < end_time)', name='time_slot_check'),
        #sa.CheckConstraint('TODO'),
        #sa.CheckConstraint('TODO'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('start_time','end_time')
        )
        op.create_table('person_role_map',
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'] ,onupdate='CASCADE', ondelete='CASCADE' ),
        sa.PrimaryKeyConstraint('person_id', 'role_id')
        )
        op.create_table('proposal',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('technical_requirements', sa.Text(), nullable=True),
        sa.Column('proposal_type_id', sa.Integer(), nullable=False),
        sa.Column('stream_id', sa.Integer(), nullable=True),
        sa.Column('travel_assistance_type_id', sa.Integer(), nullable=False),
        sa.Column('accommodation_assistance_type_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('target_audience_id', sa.Integer(), nullable=False),
        sa.Column('video_release', sa.Boolean(), nullable=True),
        sa.Column('slides_release', sa.Boolean(), nullable=True),
        sa.Column('project', sa.Text(), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('abstract_video_url', sa.Text(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        ##sa.CheckConstraint('TODO'),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['accommodation_assistance_type_id'], ['accommodation_assistance_type.id'], ),
        sa.ForeignKeyConstraint(['proposal_type_id'], ['proposal_type.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['proposal_status.id'], ),
        sa.ForeignKeyConstraint(['stream_id'], ['stream.id'], ),
        sa.ForeignKeyConstraint(['target_audience_id'], ['target_audience.id'], ),
        sa.ForeignKeyConstraint(['travel_assistance_type_id'], ['travel_assistance_type.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('special_registration',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_number', sa.Text(), nullable=True),
        sa.Column('special_offer_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['special_offer_id'], ['special_offer.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('invoice',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('manual', sa.Boolean(), nullable=False),
        sa.Column('void', sa.String(), nullable=True),
        sa.Column('issue_date', sa.DateTime(), nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('funding',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=True),
        sa.Column('status_id', sa.Integer(), nullable=True),
        sa.Column('funding_type_id', sa.Integer(), nullable=True),
        sa.Column('male', sa.Boolean(), nullable=True),
        sa.Column('why_attend', sa.Text(), nullable=True),
        sa.Column('how_contribute', sa.Text(), nullable=True),
        sa.Column('financial_circumstances', sa.Text(), nullable=True),
        sa.Column('diverse_groups', sa.Text(), nullable=True),
        sa.Column('supporting_information', sa.Text(), nullable=True),
        sa.Column('prevlca', sa.String(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['funding_type_id'], ['funding_type.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['funding_status.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('person_id','funding_type_id')
        )
        op.create_table('voucher',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('leader_id', sa.Integer(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['leader_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
        )
        op.create_table('person_social_network_map',
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('social_network_id', sa.Integer(), nullable=False),
        sa.Column('account_name', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['social_network_id'], ['social_network.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.PrimaryKeyConstraint('person_id', 'social_network_id'),
        sa.UniqueConstraint('person_id','social_network_id')
        )
        op.create_table('product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=False),
        sa.Column('auth', sa.Text(), nullable=True),
        sa.Column('validate', sa.Text(), nullable=True),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['category_id'], ['product_category.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('category_id','description')
        )
        op.create_table('db_content',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('publish_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['type_id'], ['db_content_type.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('review',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('proposal_id', sa.Integer(), nullable=False),
        sa.Column('reviewer_id', sa.Integer(), nullable=False),
        sa.Column('stream_id', sa.Integer(), nullable=True),
        sa.Column('miniconf', sa.Text(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('private_comment', sa.Text(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
        sa.ForeignKeyConstraint(['reviewer_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['stream_id'], ['stream.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('proposal_id','reviewer_id', name='ux_review_proposal_reviewer')
        )
        op.create_table('person_proposal_map',
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('proposal_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.PrimaryKeyConstraint('person_id', 'proposal_id')
        )
        op.create_table('event',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('proposal_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('publish', sa.Boolean(), nullable=False),
        sa.Column('exclusive', sa.Boolean(), nullable=False),
        sa.Column('sequence', sa.Integer(), nullable=False),
        #sa.CheckConstraint('TODO'),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
        sa.ForeignKeyConstraint(['type_id'], ['event_type.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('proposal_id')
        )
        op.create_table('volunteer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('areas', sa.String(), nullable=False),
        sa.Column('other', sa.Text(), nullable=False),
        sa.Column('experience', sa.Text(), nullable=True),
        sa.Column('accepted', sa.Boolean(), nullable=True),
        sa.Column('ticket_type_id', sa.Integer(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['ticket_type_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('person_id')
        )
        op.create_table('product_include',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('include_category_id', sa.Integer(), nullable=False),
        sa.Column('include_qty', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['include_category_id'], ['product_category.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('product_id', 'include_category_id')
        )
        op.create_table('registration',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=True),
        sa.Column('over18', sa.Boolean(), nullable=True),
        sa.Column('nick', sa.Text(), nullable=True),
        sa.Column('shell', sa.Text(), nullable=True),
        sa.Column('editor', sa.Text(), nullable=True),
        sa.Column('distro', sa.Text(), nullable=True),
        sa.Column('vcs', sa.Text(), nullable=True),
        sa.Column('silly_description', sa.Text(), nullable=True),
        sa.Column('keyid', sa.Text(), nullable=True),
        sa.Column('planetfeed', sa.Text(), nullable=True),
        sa.Column('voucher_code', sa.Text(), nullable=True),
        sa.Column('diet', sa.Text(), nullable=True),
        sa.Column('special', sa.Text(), nullable=True),
        sa.Column('partner_name', sa.Text(), nullable=True),
        sa.Column('partner_email', sa.Text(), nullable=True),
        sa.Column('partner_mobile', sa.Text(), nullable=True),
        sa.Column('prevlca', sa.String(), nullable=True),
        sa.Column('signup', sa.String(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['voucher_code'], ['voucher.code'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('person_id'),
        sa.UniqueConstraint('voucher_code')
        )
        op.create_table('attachment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('proposal_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.Text(), nullable=False),
        sa.Column('content_type', sa.Text(), nullable=False),
        sa.Column('content', sa.LargeBinary(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_creation_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('invoice_item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('invoice_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('free_qty', sa.Integer(), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('funding_attachment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('funding_id', sa.Integer(), nullable=True),
        sa.Column('filename', sa.Text(), nullable=False),
        sa.Column('content_type', sa.Text(), nullable=False),
        sa.Column('content', sa.LargeBinary(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_creation_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['funding_id'], ['funding.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('product_ceiling_map',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('ceiling_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ceiling_id'], ['ceiling.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('product_id', 'ceiling_id')
        )
        op.create_table('funding_review',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('funding_id', sa.Integer(), nullable=False),
        sa.Column('reviewer_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['funding_id'], ['funding.id'], ),
        sa.ForeignKeyConstraint(['reviewer_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('funding_id','reviewer_id')
        )
        op.create_table('payment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('invoice_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('voucher_product',
        sa.Column('voucher_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('percentage', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.ForeignKeyConstraint(['voucher_id'], ['voucher.id'], ),
        sa.PrimaryKeyConstraint('voucher_id', 'product_id')
        )
        op.create_table('registration_product_map',
        sa.Column('registration_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.ForeignKeyConstraint(['registration_id'], ['registration.id'], ),
        sa.PrimaryKeyConstraint('registration_id', 'product_id')
        )
        op.create_table('payment_received',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('approved', sa.Boolean(), nullable=False),
        sa.Column('validation_errors', sa.String(), nullable=True),
        sa.Column('payment_id', sa.Integer(), nullable=True),
        sa.Column('invoice_id', sa.Integer(), nullable=True),
        sa.Column('success_code', sa.String(), nullable=False),
        sa.Column('amount_paid', sa.Integer(), nullable=True),
        sa.Column('currency_used', sa.String(), nullable=True),
        sa.Column('auth_code', sa.String(), nullable=True),
        sa.Column('card_name', sa.String(), nullable=True),
        sa.Column('card_type', sa.String(), nullable=True),
        sa.Column('card_number', sa.String(), nullable=True),
        sa.Column('card_expiry', sa.String(), nullable=True),
        sa.Column('card_mac', sa.String(), nullable=True),
        sa.Column('gateway_ref', sa.String(), nullable=True),
        sa.Column('response_text', sa.String(), nullable=False),
        sa.Column('client_ip_zk', sa.String(), nullable=False),
        sa.Column('client_ip_gateway', sa.String(), nullable=False),
        sa.Column('email_address', sa.String(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
        sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('time_slot_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('overflow', sa.Boolean(), nullable=True),
        sa.Column('video_url', sa.Text(), nullable=True),
        sa.Column('audio_url', sa.Text(), nullable=True),
        sa.Column('slide_url', sa.Text(), nullable=True),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        #sa.CheckConstraint('TODO'),
        sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
        sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
        sa.ForeignKeyConstraint(['time_slot_id'], ['time_slot.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('time_slot_id','location_id')
        )
        op.create_table('rego_note',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rego_id', sa.Integer(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('by_id', sa.Integer(), nullable=False),
        sa.Column('creation_timestamp', sa.DateTime(), nullable=False),
        sa.Column('last_modification_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['by_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['rego_id'], ['registration.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('payment_allocation',
        sa.Column('invoice_item_id', sa.Integer(), nullable=False),
        sa.Column('payment_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['invoice_item_id'], ['invoice_item.id'],onupdate='CASCADE', ondelete='CASCADE' ),
        sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], onupdate='CASCADE', ondelete='CASCADE' ),
        sa.PrimaryKeyConstraint('invoice_item_id', 'payment_id')
        )
    
    # Create Tables
    create_tables()
    # Start populating tables
    
    
    # Setup up a session we can use to insert rows using the ZK models
    ctx = op.get_context()
    session = sa.orm.sessionmaker()
    session = session(bind=ctx.connection)
    
    add_roles(session)
    add_people(session)
    add_social_media(session)
    add_product_categories(session)
    add_ceilings(session)
    add_products(session)
    
    add_proposals(session)
    

    add_db_content_types(session)
    

    add_funding(session)

    add_special_offers(session)
    
    session.commit()
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_allocation')
    op.drop_table('rego_note')
    op.drop_table('schedule')
    op.drop_table('payment_received')
    op.drop_table('registration_product_map')
    op.drop_table('voucher_product')
    op.drop_table('payment')
    op.drop_table('funding_review')
    op.drop_table('product_ceiling_map')
    op.drop_table('funding_attachment')
    op.drop_table('invoice_item')
    op.drop_table('attachment')
    op.drop_table('registration')
    op.drop_table('product_include')
    op.drop_table('volunteer')
    op.drop_table('event')
    op.drop_table('person_proposal_map')
    op.drop_table('review')
    op.drop_table('db_content')
    op.drop_table('product')
    op.drop_table('person_social_network_map')
    op.drop_table('voucher')
    op.drop_table('funding')
    op.drop_table('invoice')
    op.drop_table('special_registration')
    op.drop_table('proposal')
    op.drop_table('person_role_map')
    op.drop_table('time_slot')
    op.drop_table('role')
    op.drop_table('product_category')
    op.drop_table('social_network')
    op.drop_table('person')
    op.drop_table('event_type')
    op.drop_table('location')
    op.drop_table('ceiling')
    op.drop_table('proposal_status')
    op.drop_table('special_offer')
    op.drop_table('funding_status')
    op.drop_table('stream')
    op.drop_table('password_reset_confirmation')
    op.drop_table('funding_type')
    op.drop_table('db_content_type')
    op.drop_table('vote')
    op.drop_table('target_audience')
    op.drop_table('proposal_type')
    op.drop_table('accommodation_assistance_type')
    op.drop_table('travel_assistance_type')
    op.drop_table('url_hash')
    ### end Alembic commands ###
