import sqlalchemy.types as types

class CommaList(types.TypeDecorator):
    """Store a set as a comma-separated list in a text field."""
    impl = types.String
    def convert_bind_param(self, value, engine):
        """ convert from zookeepr to database representation """
        if value is None:
            return None
        print "foo",`value`
        return ','.join(value)
    def convert_result_value(self, value, engine):
        """ convert from database to zookeepr representation """
        print "bar", `value`
        if value is None:
            return None
        return value.split(',')
