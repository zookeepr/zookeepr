import sqlalchemy as sa

from meta import Base, Session, metadata

from pylons.controllers.util import abort

from product import Product
from person import Person

def setup(meta):
    pass

# for doing n-n mappings of FulfilmentType and FulfilmentStatus
fulfilment_type_status_map = sa.Table('fulfilment_type_status_map', metadata,
        sa.Column(
            'fulfilment_type_id', sa.types.Integer,
            sa.ForeignKey(
                'fulfilment_type.id', ondelete='CASCADE', onupdate='CASCADE'
            ), primary_key=True, nullable=False),
        sa.Column(
            'fulfilment_status_id', sa.types.Integer,
            sa.ForeignKey(
                'fulfilment_status.id', ondelete='CASCADE', onupdate='CASCADE'
            ), primary_key=True, nullable=False)
)

class FulfilmentStatus(Base):
    """ Status of fulfilment
    """
    # table
    __tablename__ = 'fulfilment_status'

    # columns
    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, unique=True, nullable=False)
    locked = sa.Column(sa.types.Boolean, nullable=False, default=False)
    void = sa.Column(sa.types.Boolean, nullable=False, default=False)
    completed = sa.Column(sa.types.Boolean, nullable=False, default=False)

    # relations

    # methods
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(cls).get(id)
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(cls).order_by(cls.name).all()

    def __init__(self, **kwargs):
        super(FulfilmentStatus, self).__init__(**kwargs)

    def __repr__(self):
        return '<FulfilmentStatus id=%r name=%r>' % (self.id, self.name)

class FulfilmentType(Base):
    """ Types of fulfilment
    """
    # table
    __tablename__ = 'fulfilment_type'

    # columns
    id = sa.Column(sa.types.Integer, primary_key=True)
    initial_status_id = sa.Column(sa.types.Integer, sa.ForeignKey('fulfilment_status.id'), nullable=False)
    name = sa.Column(sa.types.Text, unique=True, nullable=False)

    # relations
    status = sa.orm.relation(FulfilmentStatus,
        secondary=fulfilment_type_status_map, backref='types')
    initial_status = sa.orm.relation(FulfilmentStatus)

    # methods
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(cls).get(id)
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(cls).order_by(cls.name).all()

    def __init__(self, **kwargs):
        super(FulfilmentType, self).__init__(**kwargs)

    def __repr__(self):
        return '<FulfilmentType id=%r name=%r>' % (self.id, self.name)

# for doing n-n mappings of Fulfilment and FulfilmentGroup
fulfilment_group_map = sa.Table('fulfilment_group_map', metadata,
        sa.Column(
            'fulfilment_id', sa.types.Integer,
            sa.ForeignKey(
                'fulfilment.id', ondelete='CASCADE', onupdate='CASCADE'
            ), primary_key=True, nullable=False),
        sa.Column(
            'fulfilment_group_id', sa.types.Integer,
            sa.ForeignKey(
                'fulfilment_group.id', ondelete='CASCADE', onupdate='CASCADE'
            ), primary_key=True, nullable=False)
)

class FulfilmentGroup(Base):
    """ Fulfilment Group
    """
    # table
    __tablename__ = 'fulfilment_group'

    id = sa.Column(sa.types.Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=True)
    code = sa.Column(sa.types.Text, unique=True)

    # relations
    person = sa.orm.relation(Person, backref='fulfilment_groups')

    # methods
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(cls).get(id)
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(cls).order_by(cls.person_id).all()

    def __init__(self, **kwargs):
        super(FulfilmentGroup, self).__init__(**kwargs)

    def __repr__(self):
        return '<FulfilmentGroup id=%r group=%r>' % (self.id, self.name)

class Fulfilment(Base):
    """ Stores details of order fulfilment
    """
    # table
    __tablename__ = 'fulfilment'

    id = sa.Column(sa.types.Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'),
        nullable=False)
    type_id = sa.Column(sa.types.Integer, sa.ForeignKey('fulfilment_type.id'),
        nullable=False)
    status_id = sa.Column(sa.types.Integer, sa.ForeignKey('fulfilment_status.id'),
        nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False,
        default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False,
        default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # mapped attributes
    is_void = sa.orm.column_property(
        sa.select([FulfilmentStatus.void]).\
        where('fulfilment.status_id = fulfilment_status.id').\
        correlate_except(FulfilmentStatus)
    )
    is_completed = sa.orm.column_property(
        sa.select([FulfilmentStatus.completed]).\
        where('fulfilment.status_id = fulfilment_status.id').\
        correlate_except(FulfilmentStatus)
    )
    is_locked = sa.orm.column_property(
        sa.select([FulfilmentStatus.locked]).\
        where('fulfilment.status_id = fulfilment_status.id').\
        correlate_except(FulfilmentStatus)
    )
    can_edit = sa.orm.column_property(
        sa.select([sa.not_(sa.or_(FulfilmentStatus.completed, FulfilmentStatus.void, FulfilmentStatus.locked))]).\
        where('fulfilment.status_id = fulfilment_status.id').\
        correlate_except(FulfilmentStatus)
    )

    # relations
    person = sa.orm.relation(Person, backref='fulfilments')
    type = sa.orm.relation(FulfilmentType)
    status = sa.orm.relation(FulfilmentStatus)
    groups = sa.orm.relation(FulfilmentGroup, secondary=fulfilment_group_map, backref='fulfilments')

    # methods
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(cls).get(id)
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(cls).order_by(cls.id).all()

    def __init__(self, **kwargs):
        super(Fulfilment, self).__init__(**kwargs)
        if not 'status' in kwargs and self.type:
            self.status_id = self.type.initial_status_id

    def __repr__(self):
        return '<Fulfilment id=%r person=%r>' % (self.id, self.person_id)

class FulfilmentItem(Base):
    """ Fulfilment Items
    """
    # table
    __tablename__ = 'fulfilment_item'

    id = sa.Column(sa.types.Integer, primary_key=True)
    fulfilment_id = sa.Column(sa.types.Integer, sa.ForeignKey('fulfilment.id'),
        nullable=False)
    product_id = sa.Column(sa.types.Integer, sa.ForeignKey('product.id'),
        nullable=False)
    product_text = sa.Column(sa.types.Text, unique=True, nullable=True)
    qty = sa.Column(sa.types.Integer, nullable=False)

    # relations
    fulfilment = sa.orm.relation(Fulfilment,
        backref=sa.orm.backref('items', cascade="all, delete-orphan"))
    product = sa.orm.relation(Product, backref='fulfilment_items')
