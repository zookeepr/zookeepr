from datetime import datetime
import os, random, re, urllib
from zookeepr.lib import helpers as h
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
          ('/ceiling', '''Manage ceilings and available inventory. [Inventory]'''),
          ('/registration', '''View registrations and delegate details. [Registrations]'''),
          ('/invoice', '''View assigned invoices and their status. [Registrations]'''),
          ('/volunteer', '''View and approve/deny applications for volunteers. [Registrations]'''),
          ('/rego_note', '''Create and manage private notes on individual registrations. [Registrations]'''),
          ('/role', '''Add, delete and modify available roles. View the person list to actually assign roles. [Accounts]'''),

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
        pat = re.compile(r'\[([\ a-zA-Z,]+)\]')
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

    def activate_talks(self):
        """
        Set the talks to accepted as per the list in the admin controller. [Schedule]
        """
        # {theatre: [id's]}
        keynotes = {'Stanley Burbury': (227)}
        miniconfs = {'Unknown': (8,32,157,83,108,49,132,9,26,116,121,201)}
        tutorials = {'Stanley Burbury 1': (40,143),
                     'Arts Lecture Theatre': (43,181),
                     'Stanley Burbury 2': (164,151),
                     'Social Science 1': (112,5),
                     'Social Science 2': (198,89)}
        presentations = {'Stanley Burbury 1': (51,205,11,225,219,48,87,90,156,175,203,189,126),
                     'Arts Lecture Theatre': (218,173,22,84,131,45,56,13,91,178,106,171,30),
                     'Stanley Burbury 2': (136,12,78,99,209,122,29,179,210,64,79,33,105),
                     'Social Science 1': (77,148,208,52,66,187,93,139,158,176,166,76,172),
                     'Social Science 2': (149,123,211,192,67,161,160,119,152,46,145,72,217)}
        
        sql_execute("UPDATE proposal SET accepted = FALSE, theatre = NULL") # set all talks to unaccepted to start
        
        for collection in (keynotes, miniconfs, tutorials, presentations):
            for (room, ids) in collection.iteritems():
                if type(ids) is int:
                    ids = '(' + str(ids) + ')'
                sql_execute("UPDATE proposal SET theatre = '%s', accepted = TRUE WHERE id IN %s" % (room, str(ids)))
        c.text = "<p>Updated successfully</p>"
        return render_response("admin/text.myt")

    def rej_papers_abstracts(self):
        """ Rejected papers, with abstracts (for the miniconf organisers)
        [Schedule] """
        return sql_response("""
SELECT
    proposal.id, 
    proposal.title, 
    proposal_type.name AS "proposal type",
    proposal.project,
    proposal.url as project_url,
    proposal.abstract,
    person.firstname || ' ' || person.lastname as name,
    person.email_address,
    person.url as homepage,
    person.bio,
    person.experience,
    stream.name AS stream,
    MAX(review.score),
    MIN(review.score),
    AVG(review.score)
FROM proposal 
    LEFT JOIN review ON (proposal.id=review.proposal_id)
    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
    LEFT JOIN stream ON (review.stream_id=stream.id)
    LEFT JOIN person_proposal_map ON (proposal.id = person_proposal_map.proposal_id)
    LEFT JOIN person ON (person_proposal_map.person_id = person.id)
WHERE
    review.stream_id = (SELECT review2.stream_id FROM review review2 WHERE review2.proposal_id = proposal.id GROUP BY review2.stream_id ORDER BY count(review2.stream_id) DESC LIMIT 1)
    AND proposal.proposal_type_id != 2
    AND proposal.accepted = False
GROUP BY proposal.id, proposal.title, proposal_type.name, stream.name, person.firstname, person.lastname, person.email_address, person.url, person.bio, person.experience, proposal.abstract, proposal.project, proposal.url
ORDER BY proposal.id ASC, stream.name, proposal_type.name ASC, max DESC, min DESC, avg DESC, proposal.id ASC
        """)

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
ORDER BY stream.name, proposal_type.name ASC, max DESC, min DESC, avg DESC, proposal.id ASC
""")

    def countdown(self):
        """ How many days until conference opens """
        timeleft = lca_info['date'] - datetime.now()
        res = Response ("%.1f days" % (timeleft.days +
                                               timeleft.seconds / (3600*24.)))
        res.headers['Refresh'] = 3600
        return res
        
    def registered_speakers(self):
        """ Listing of speakers and various stuff about them [Speakers] """
        """ HACK: This code should be in the registration controller """
        import re
        shirt_totals = {}
        c.data = []
        c.noescape = True
        cons_list = ('speaker_record', 'speaker_video_release', 'speaker_slides_release')
        speaker_list = []
        for p in self.dbsession.query(Person).all():
            if not p.is_speaker(): continue
            speaker_list.append((p.lastname.lower()+' '+p.firstname, p))
        speaker_list.sort()

        for (sortkey, p) in speaker_list:
            registration_link = ''
            if p.registration:
                registration_link = '<a href="/registration/%d">Details</a>, ' % (p.registration.id)
            res = [
      '<a href="/person/%d">%s %s</a> (%s<a href="mailto:%s">email</a>)'
                  % (p.id, p.firstname, p.lastname, registration_link, p.email_address)
            ]

            talks = [talk for talk in p.proposals if talk.accepted]
            res.append('; '.join([
                '<a href="/programme/schedule/view_talk/%d">%s</a>'
                                % (t.id, h.truncate(t.title)) for t in talks]))
            if p.registration:
              if p.invoices:
                if p.valid_invoice() is None:
                    res.append('Invalid Invoice')
                else:
                    if p.valid_invoice().paid():
                      res.append('<a href="/invoice/%d">Paid $%.2f</a>'%(
                               p.valid_invoice().id, p.valid_invoice().total()/100.0) )
                    else:
                      res.append('<a href="/invoice/%d">Owes $%.2f</a>'%(
                               p.valid_invoice().id, p.valid_invoice().total()/100.0) )
                    
                    shirt = ''
                    for item in p.valid_invoice().items:
                        if ((item.description.lower().find('shirt') is not -1) and (item.description.lower().find('discount') is -1)):
                            shirt += item.description + ', '
                            if shirt_totals.has_key(item.description):
                                shirt_totals[item.description] += 1
                            else:
                                shirt_totals[item.description] = 1
                    res.append(shirt)
              else:
                res.append('No Invoice')
                res.append('-')

              cons = [con.replace('_', ' ') for con in cons_list
                                           if getattr(p.registration, con)] 
              if len(cons)==3:
                res.append('Release All')
              elif len(cons)==0:
                res.append('None')
              else:
                res.append(' and '.join(cons))

              res.append('<br><br>'.join(["<b>Note by <i>" + n.by.firstname + " " + n.by.lastname + "</i> at <i>" + n.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") + "</i>:</b><br>" + h.line_break(n.note) for n in p.registration.notes]))
              if p.registration.diet:
                  res[-1] += '<br><br><b>Diet:</b> %s' % (p.registration.diet)
              if p.registration.special:
                  res[-1] += '<br><br><b>Special Needs:</b> %s' % (p.registration.special)
            else:
              res+=['Not Registered', '', '', '']
            #res.append(`dir(p.registration)`)
            c.data.append(res)

        # sort by rego status (while that's important)
        def my_cmp(a,b):
            return cmp('OK' in a[4], 'OK' in b[4])
        c.data.sort(my_cmp)

        c.columns = ('Name', 'Talk(s)', 'Status', 'Shirts', 'Concent', 'Notes')
        c.text = "<p>Shirt Totals:"
        for key, value in shirt_totals.items():
            c.text += "<br>" + str(key) + ": " + str(value)
        c.text += "</p>"
        return render_response('admin/table.myt')

    def reconcile(self):
        """ Reconcilliation between D1 and ZK; for now, compare the D1 data
        that have been placed in the fixed location in the filesystem and
        work from there... [Registrations] """
        import csv
        d1_data = csv.reader(file('/srv/zookeepr/reconcile.d1'))
        d1_cols = d1_data.next()
        d1_cols = [s.strip() for s in d1_cols]

        all = {}

        t_offs = d1_cols.index('payment_id')
        amt_offs = d1_cols.index('payment_amount')
        d1 = {}
        for row in d1_data:
          t = row[t_offs]
          amt = row[amt_offs]
          if amt[-3]=='.':
            # remove the decimal point
            amt = amt[:-3] + amt[-2:]
          row.append(amt)
          all[t] = 1
          if d1.has_key(t):
            d1[t].append(row)
          else:
            d1[t] = [row]

        zk = {}
        for p in self.dbsession.query(PaymentReceived).all():
          t = p.TransID
          all[t] = 1
          if zk.has_key(t):
            zk[t].append(p)
          else:
            zk[t] = [p]
          
        zk_fields =  ('InvoiceID', 'TransID', 'Amount', 'AuthNum',
                                'Status', 'result', 'HTTP_X_FORWARDED_FOR')

        all = all.keys()
        all.sort()
        c.data = []
        for t in all:
          zk_t = zk.get(t, []); d1_t = d1.get(t, [])
          if len(zk_t)==1 and len(d1_t)==1:
            if str(zk_t[0].Amount) == d1_t[0][-1]:
              continue
          c.data.append((
            '; '.join([', '.join([str(getattr(z, f)) for f in zk_fields])
                                                              for z in zk_t]),
            t,
            '; '.join([', '.join(d) for d in d1_t])
          ))

        return render_response('admin/table.myt')

    def linux_australia_signup(self):
        """ People who ticked "I want to sign up for (free) Linux Australia
        membership!" [Mailing Lists] """

        c.text = """<p>People who ticked "I want to sign up for (free) Linux
        Australia membership!" (whether or not they then went on to pay for
        the conference).</p>"""
        
        query = """SELECT person.firstname, person.lastname, 
                    person.address1, person.address2, person.city, person.state, person.postcode, person.country,
                    person.phone, person.mobile, person.company,
                    registration.creation_timestamp
                   FROM person
                   LEFT JOIN registration ON (person.id = registration.person_id)
                   WHERE registration.lasignup = True
                """

        return sql_response(query)

    def lca_announce_signup(self):
        """ People who ticked "I want to sign up to the low traffic conference announcement mailing list!" [Mailing Lists] """

        c.text = """<p>People who ticked "I want to sign up to the low traffic conference 
        announcement mailing list!" (whether or not they then went on to pay for
        the conference).</p><p>Copy and paste the following into mailman</p>
        <p><textarea cols="100" rows="25">"""

        count = 0
        for r in self.dbsession.query(Registration).all():
            if not r.announcesignup:
                continue
            p = r.person
            c.text += p.firstname + " " + p.lastname + " &lt;" + p.email_address + "&gt;\n"
            count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return render_response('admin/text.myt')

    def lca_chat_signup(self):
        """ People who ticked "I want to sign up to the conference attendees mailing list!" [Mailing Lists] """

        c.text = """<p>People who ticked "I want to sign up to the conference attendees mailing list!" (whether or not they then went on to pay for
        the conference).</p><p>Copy and paste the following into mailman</p>
        <p><textarea cols="100" rows="25">"""

        count = 0
        for r in self.dbsession.query(Registration).all():
            if not r.delegatesignup:
                continue
            p = r.person
            c.text += p.firstname + " " + p.lastname + " &lt;" + p.email_address + "&gt;\n"
            count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return render_response('admin/text.myt')

    def accom_wp_registers(self):
        """ People who selected "Wrest Point" as their accommodation option. (Includes un-paid invoices!) [Accommodation] """
        query = """SELECT person.firstname || ' ' || person.lastname as name, person.email_address, invoice.id AS "Invoice ID" FROM person
                    LEFT JOIN invoice ON (invoice.person_id = person.id)
                    LEFT JOIN invoice_item ON (invoice_item.invoice_id = invoice.id)
                    WHERE invoice_item.product_id = 28 AND invoice.void = FALSE"""
        return sql_response(query)

    def accom_uni_registers(self):
        """ People who selected any form as university accommodation. (Includes un-paid invoices!) [Accommodation] """
        query = """SELECT person.firstname || ' ' || person.lastname as name, person.email_address, invoice.id AS "Invoice ID" FROM person
                    LEFT JOIN invoice ON (invoice.person_id = person.id)
                    LEFT JOIN invoice_item ON (invoice_item.invoice_id = invoice.id)
                    WHERE invoice_item.product_id IN (29,38,39,40,41,42) AND invoice.void = FALSE"""
        return sql_response(query)

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

def sql_execute(sql):
    import zookeepr.model
    res = zookeepr.model.metadata.bind.execute(sql)
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
    res = zookeepr.model.metadata.bind.execute(sql)
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
