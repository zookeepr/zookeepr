from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole

class AdminController(SecureController):
    """ Miscellaneous admin tasks. """

    permissions = { 'ALL': [AuthRole('organiser')] }

    def test(self):
        """
	Testing, testing, 1, 2, 3.
        """
        return Response("This is a test. Hope you've studied!")

def sql_response(sql):
    """ This function bypasses all the MVC stuff and just puts up a table
    of results from the given SQL statement.

    Ideally, of course, it should never be used.

    Example:
	def foo(self):
	    return sql_response('select * from person')
    """
    import zookeepr.model
    res = zookeepr.model.metadata.get_engine().execute(sql);
    c.columns = res.keys
    c.data = res.fetchall()
    c.sql = sql
    return render_response('admin/sqltable.myt')
    
def sql_data(sql):
    """ This function bypasses all the MVC stuff and just gives you a
    two-dimensional array based on the given SQL statement.

    Ideally, of course, it should never be used.
    """
    import zookeepr.model
    return zookeepr.model.metadata.get_engine().execute(sql).fetchall();
