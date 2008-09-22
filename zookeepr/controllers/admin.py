from datetime import datetime
import os, random, re, urllib
from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole, AuthTrue
from zookeepr.controllers.proposal import Proposal
from zookeepr.model import Registration, Person, Invoice, PaymentReceived
from zookeepr.model.registration import RegoNote
from zookeepr.config.lca_info import lca_info

class AdminController(SecureController):
    """ Miscellaneous admin tasks. """

    permissions = {
      'ALL': [AuthRole('organiser')],
      'proposals_by_strong_rank': [AuthRole('reviewer')],
      'proposals_by_max_rank': [AuthRole('reviewer')],
      'proposals_by_stream': [AuthRole('reviewer')]
    }
    def index(self):
        res = dir(self)
        exceptions = ['check_permissions', 'dbsession',
                     'index', 'logged_in', 'permissions', 'start_response']

        # get the ones in this controller by introspection.
        funcs = [('/admin/'+x, getattr(self, x).__doc__ or '')
                       for x in res if x[0] != '_' and x not in exceptions]

        # other functions should be appended to the list here.
        funcs += [
          ('/db_content', '''Edit HTML pages that are stored in the database. [Content]'''),
          ('/db_content/list_files', '''List and upload files for use on the site. [Content]'''),
          ('/person', '''List of people signed up to the webpage (with option to view/change their zookeepr roles) [Accounts]'''),
          ('/product', '''Manage all of zookeeprs products. [Inventory]'''),
          ('/voucher', '''Manage vouchers to give to delegates. [Inventory]'''),
          ('/ceilings', '''Manage ceilings and available inventory. [Inventory]'''),
          ('/registration', '''View registrations and delegate details. [Registrations]'''),
          ('/invoice', '''View assigned invoices and their status. [Registrations]'''),

           #('/accommodation', ''' [accom] '''),
           #('/voucher_code', ''' Voucher codes [rego] '''),
           #('/invoice/remind', ''' '''),
           #('/openday', ''' '''),
           #('/registration', ''' Summary of registrations, including summary
          #of accommodation [rego,accom] '''),
           #('/invoice', ''' List of invoices (that is, registrations). This
          #is probably the best place to check whether a given person has or
          #hasn't registered and/or paid. [rego] '''),
           #('/pony', ''' OMG! Ponies!!! [ZK]'''),

          ('/review/help', ''' Information on how to get started reviewing [CFP] '''),
          ('/proposal/review_index', ''' To see what you need to reveiw [CFP] '''),
          ('/review', ''' To see what you have reviewed [CFP]'''),
          ('/proposal/summary', ''' Summary of the reviewed papers [CFP] '''),
          ('/review/summary', ''' List of reviewers and scores [CFP] '''),

          #('/registration/list_miniconf_orgs', ''' list of miniconf
          #organisers (as the registration code knows them, for miniconf
          #voucher) [miniconf] '''),

        ]

        # show it!
        c.columns = ['page', 'description']
        funcs = [('<a href="%s">%s</a>'%(fn,fn), desc)
                                                   for (fn, desc) in funcs]
        sect = {}
        pat = re.compile(r'\[([a-zA-Z,]+)\]')
        for (page, desc) in funcs:
            m = pat.search(desc)
            if m:
                desc = pat.sub(r'<small>[\1]</small>', desc)
                for s in m.group(1).split(','):
                    sect[s] = sect.get(s, []) + [(page, desc)]
            else:
                sect['Other'] = sect.get('Other', []) + [(page, desc)]
        c.text = '<div class = \'contents\'>\n\t\t\t<h3>Admin functions</h3>\n\t\t\t<ul>\n\t\t\t\t<li>'
        c.noescape = True

        sects = [(s.lower(), s) for s in sect.keys()]; sects.sort()
        c.text += '\t\t\t\t<li>'.join(['<a href="#%s">%s</a></li>\n'%(s, s)
                                                  for s_lower, s in sects])
        c.text += '\t\t\t</ul>\n\t\t\t</div>'
        for s_lower, s in sects:
            c.text += '<a name="%s"></a>' % s
            c.text += '<h2>%s</h2>' % s
            c.data = sect[s]
            c.text = render('admin/table.myt', fragment=True)
        return render_response('admin/text.myt')

    def collect_garbage(self):
        """
        Invoke the garbage collector. [ZK]
        """
        import gc
        before = len(gc.get_objects())
        garbage = gc.collect()
        after = len(gc.get_objects())
        uncollectable = len(gc.garbage)
        del(gc.garbage[:])
        return Response("""
        Is automatic garbage collection enabled? %s.
        <br>Garbage collector knows of %d objects.
        <br>Full collection: %d pieces of garbage found, %d uncollectable.
        <br>Garbage collector knows of %d objects.
        """ % (
          gc.isenabled(),
          before,
          garbage, uncollectable,
          after,
        ))
    def known_objects(self):
        """
        List known objects by type. (Invokes GC first.) [ZK]
        """
        import gc
        gc.collect()
        count = {}
        objects = gc.get_objects()
        for o in objects:
          t = type(o)
          count[t] = count.get(t, 0) + 1
        total = len(objects); scale = 100.0 / total
        objects = None #avoid having the data twice...
        c.data = [(num, '%.1f%%' % (num * scale), t)
                                         for (t, num) in count.iteritems()]
        c.data.sort(reverse=True)
        c.columns = 'count', '%', 'type'
        c.text = "Total: %d" % total
        return render_response('admin/table.myt')

    def list_attachments(self):
        """ List of attachments [CFP] """
        return sql_response('''
        select title, filename from attachment, proposal where proposal.id=proposal_id;

        ''')
    def person_creation(self):
        """ When did people create their accounts? [Accounts] """
        return sql_response("""select person.id, firstname || ' ' ||
        lastname as name, creation_timestamp as created from person
        order by person.id;
        """)
    def auth_users(self):
        """ List of users that are authorised for some role [Accounts] """
        return sql_response("""select role.name as role, firstname || ' '
        || lastname as name, email_address, person.id
        from role, person, person_role_map
        where person.id=person_id and role.id=role_id
        order by role, lastname, firstname""")

    def proposal_list(self):
        """ Large table of all the proposals, presenters and dates. [CFP] """
        return sql_response("""
          SELECT proposal.*,
            person.firstname || ' ' || person.lastname as name, person.email_address, person.address1, person.address2, person.city, person.state, person.postcode, person.country, person.company, person.phone, person.mobile, person.url, person.experience, person.bio, person.creation_timestamp as account_creation
          FROM proposal, person, person_proposal_map
          WHERE proposal.id = person_proposal_map.proposal_id AND person.id = person_proposal_map.person_id
          ORDER BY proposal.title ASC;
        """)

    def proposals_by_strong_rank(self):
        """ List of proposals ordered by number of certain score / total number of reviewers [CFP] """
        query = """
SELECT
    proposal.id,
    proposal.title,
    proposal_type.name AS "proposal type",
    review.score,
    COUNT(review.id) AS "#reviewers at this score",
    (
        SELECT COUNT(review2.id)
            FROM review as review2
            WHERE review2.proposal_id = proposal.id
    ) AS "#total reviewers",
    CAST(
        CAST(
            COUNT(review.id) AS float(8)
        ) / CAST(
            (SELECT COUNT(review2.id)
                FROM review as review2
                WHERE review2.proposal_id = proposal.id
            ) AS float(8)
        ) AS float(8)
    ) AS "#reviewers at this score / #total reviews %%"
FROM proposal
    LEFT JOIN review ON (proposal.id=review.proposal_id)
    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
WHERE
    (
        SELECT COUNT(review2.id)
            FROM review as review2
            WHERE review2.proposal_id = proposal.id
    ) != 0
GROUP BY proposal.id, proposal.title, review.score, proposal_type.name
ORDER BY proposal_type.name ASC, review.score DESC, "#reviewers at this score / #total reviews %%" DESC, proposal.id ASC"""

        return sql_response(query)

    def proposals_by_max_rank(self):
        """ List of all the proposals ordered max score, min score then average [CFP] """
        return sql_response("""
SELECT
    proposal.id,
    proposal.title,
    proposal_type.name AS "proposal type",
    MAX(review.score),
    MIN(review.score),
    AVG(review.score)
FROM proposal
    LEFT JOIN review ON (proposal.id=review.proposal_id)
    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
GROUP BY proposal.id, proposal.title, proposal_type.name
ORDER BY proposal_type.name ASC, max DESC, min DESC, avg DESC, proposal.id ASC
""")

    def proposals_by_stream(self):
        """ List of all the proposals ordered by stream, max score, min score then average [CFP] """
        return sql_response("""
SELECT
    proposal.id, 
    proposal.title, 
    proposal_type.name AS "proposal type",
    stream.name AS stream,
    MAX(review.score),
    MIN(review.score),
    AVG(review.score)
FROM proposal 
    LEFT JOIN review ON (proposal.id=review.proposal_id)
    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
    LEFT JOIN stream ON (review.stream_id=stream.id)
WHERE review.stream_id = (SELECT review2.stream_id FROM review review2 WHERE review2.proposal_id = proposal.id GROUP BY review2.stream_id ORDER BY count(review2.stream_id) DESC LIMIT 1)
GROUP BY proposal.id, proposal.title, proposal_type.name, stream.name
ORDER BY proposal_type.name ASC, max DESC, min DESC, avg DESC, proposal.id ASC
""")

    def countdown(self):
        """ How many days until conference opens """
        timeleft = lca_info['date'] - datetime.now()
        res = Response ("%.1f days" % (timeleft.days +
                                               timeleft.seconds / (3600*24.)))
        res.headers['Refresh'] = 3600
        return res

def csv_response(sql):
    import zookeepr.model
    res = zookeepr.model.metadata.bind.execute(sql);
    c.columns = res.keys
    c.data = res.fetchall()
    c.sql = sql

    import csv, StringIO
    f = StringIO.StringIO()
    w = csv.writer(f)
    w.writerow(c.columns)
    w.writerows(c.data)
    res = Response(f.getvalue())
    res.headers['Content-type']='text/plain; charset=utf-8'
    res.headers['Content-Disposition']='attachment; filename="table.csv"'
    return res

def sql_response(sql):
    """ This function bypasses all the MVC stuff and just puts up a table
    of results from the given SQL statement.

    Ideally, of course, it should never be used.

    Example:
        def foo(self):
            return sql_response('select * from person')
    """
    if request.GET.has_key('csv'):
        return csv_response(sql)
    import zookeepr.model
    res = zookeepr.model.metadata.bind.execute(sql);
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
    return zookeepr.model.metadata.bind.execute(sql).fetchall();
