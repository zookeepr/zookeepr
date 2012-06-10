import sqlalchemy.types as types

class CommaList(types.TypeDecorator):
    """Store a set as a comma-separated list in a text field."""
    impl = types.String
    def process_bind_param(self, value, engine):
        """ convert from zkpylons to database representation """
        if value is None:
            return None
        if type(value) in (str, unicode):
            return value
        return ','.join(value)

    def process_result_value(self, value, engine):
        """ convert from database to zkpylons representation """
        if value is None:
            return None
        return str(value).split(',')

    def copy(self):
            return CommaList(self.impl.length)
