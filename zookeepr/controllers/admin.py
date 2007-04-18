from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole

class AdminController(SecureController):
    """ Miscellaneous admin tasks. """

    permissions = { 'ALL': [AuthRole('organiser')] }
    def index(self):
        res = dir(self)
	exceptions = ['check_permissions', 'dbsession', 'index',
			      'logged_in', 'permissions', 'start_response']

	# get the ones in this controller by introspection.
	funcs = [('/admin/'+x, getattr(self, x).__doc__)
		       for x in res if x[0] != '_' and x not in exceptions]

        # other functions should be appended to the list here.
	funcs += [
	  ('/profile', '''List of people signed up (with option to
					      view/change their roles)'''),
	]

	# show it!
        c.columns = ['page', 'description']
	c.data = [('<a href="%s">%s</a>'%(fn,fn), desc)
						   for (fn, desc) in funcs]
        c.text = 'List of admin functions.'
	return render_response('admin/table.myt')

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
