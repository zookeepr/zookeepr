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
	  ('/profile', '''List of people signed up to the webpage (with
			   option to view/change their zookeepr roles)'''),

 	  ('/accommodation', ''' '''),
 	  ('/discount_code', ''' '''),
 	  ('/profile', ''' List of all website accounts (with links...)'''),
 	  ('/invoice/remind', ''' '''),
 	  ('/openday', ''' '''),
 	  ('/proposal', ''' '''),
 	  ('/registration', ''' '''),
 	  ('/pony', ''' OMG! Ponies!!!'''),

          ('/proposal', ''' To see what you need to reveiw '''),
          ('/review', ''' To see what you have reviewed '''),
          ('/proposal/summary', ''' summary of the reviewed papers '''),
          ('/review/summary', ''' summary of reviews '''),

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

    def list_miniconfs(self):
        """ List of miniconfs """
        return sql_response("""select proposal.id as id, title, abstract,
	proposal.url, firstname || ' ' || lastname as name, email_address from proposal,
	person, person_proposal_map, account where proposal_type_id = 2 and
	person.id=person_id and person.id=account.id and proposal.id=proposal_id order by title""")
    def list_attachments(self):
        """ List of attachments """
        return sql_response('''
	select title, filename from attachment, proposal where proposal.id=proposal_id;

	''')
    def account_creation(self):
        """ When did people create their accounts? """
	return sql_response("""select person.id, firstname || ' ' ||
	lastname as name, creation_timestamp as created from account,
	person where account.id=person.id order by person.id;
	""")
    def auth_users(self):
        """ List of users that are authorised for some role """
	return sql_response("""select role.name as role, firstname || ' '
	|| lastname as name, person.id from role, person, person_role_map
	where person.id=person_id and role.id=role_id order by role,
	lastname, firstname""")

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
