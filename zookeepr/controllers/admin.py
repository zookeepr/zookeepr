from datetime import datetime
import os, random, re, urllib
from zookeepr.lib import helpers as h
from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole, AuthTrue
from zookeepr.controllers.proposal import Proposal
from zookeepr.model import Registration, Person, Invoice, PaymentReceived, Product, InvoiceItem
from zookeepr.model.registration import RegoNote
from zookeepr.config.lca_info import lca_info, lca_rego

class AdminController(SecureController):
    """ Miscellaneous admin tasks. """

    permissions = {
      'ALL': [AuthRole('organiser')],
      'proposals_by_strong_rank': [AuthRole('reviewer')],
      'proposals_by_max_rank': [AuthRole('reviewer')],
      'proposals_by_stream': [AuthRole('reviewer')],
      'planet_lca': [AuthRole('organiser'), AuthRole('planetfeed')],
      'keysigning_conference': [AuthRole('organiser'), AuthRole('keysigning')],
      'keysigning_single': [AuthRole('organiser'), AuthRole('keysigning')],
      'keysigning_participants_list': [AuthRole('organiser'), AuthRole('keysigning')]
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
          ('/invoice', '''View assigned invoices and their status. [Invoicing]'''),
          ('/invoice/new', '''Create manual invoice for a person. [Invoicing]'''),
          ('/volunteer', '''View and approve/deny applications for volunteers. [Registrations]'''),
          ('/rego_note', '''Create and manage private notes on individual registrations. [Registrations]'''),
          ('/role', '''Add, delete and modify available roles. View the person list to actually assign roles. [Accounts]'''),
          ('/registration/generate_badges', '''Generate one or many Badges. [Registrations]'''),
          
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
        # {theatre: day: [id's]}
        keynotes = {'Stanley Burbury': {
                              'Wednesday':  (227),
                              #'Thursday':   (),
                              #'Friday':     ()
                           }
                         }
        miniconfs = {'Unknown': {
                              'Monday':  (8  , 157, 9  , 49 , 83 , 26 , 201),
                              'Tuesday': (32 , 108, 132, 116, 121) #doesn't include 2 dayers
                           }
                         }
        tutorials = {'Stanley Burbury 1': {
                              'Wednesday': (40),
                              'Thursday':  (143)
                           },
                           'Arts Lecture Theatre': {
                              'Wednesday': (43),
                              'Thursday':  (181)
                           },
                           'Stanley Burbury 2': {
                              'Wednesday': (164),
                              'Thursday':  (151)
                           },
                           'Social Science 1': {
                              'Wednesday': (112),
                              'Thursday':  (5)
                           },
                           'Social Science 2': {
                              'Wednesday': (70),
                              #'Thursday':  ()
                           }
                         }
        presentations = {'Stanley Burbury 1': {
                              'Wednesday': (51 , 205, 11 , 225),
                              'Thursday':  (219, 48 , 87 , 90),
                              'Friday':    (156, 175, 203, 189, 126)
                           },
                           'Arts Lecture Theatre': {
                              'Wednesday': (218, 173, 22 , 84 ),
                              'Thursday':  (131, 45 , 56 , 13 ),
                              'Friday':    (91 , 178, 106, 171, 30 )
                           },
                           'Stanley Burbury 2': {
                              'Wednesday': (136, 12 , 78 , 99 ),
                              'Thursday':  (228, 122, 29 , 179),
                              'Friday':    (210, 64 , 79 , 33 , 105)
                           },
                           'Social Science 1': {
                              'Wednesday': (77 , 148, 208, 52 ),
                              'Thursday':  (66 , 187, 93 , 139),
                              'Friday':    (158, 176, 166, 76 , 172)
                           },
                           'Social Science 2': {
                              'Wednesday': (149, 123, 211, 192),
                              'Thursday':  (67 , 161, 80, 117, 92 , 119),
                              'Friday':    (152, 46 , 145, 72 , 217)
                           }
                         }
        
        sql_execute("UPDATE proposal SET theatre = NULL, scheduled = NULL, accepted = FALSE") # set all talks to unaccepted to start
        
        timestamp = {'Monday':    '2009-01-19',
                     'Tuesday':   '2009-01-20',
                     'Wednesday': '2009-01-21',
                     'Thursday':  '2009-01-22',
                     'Friday':    '2009-01-23'}
        for collection in (keynotes, miniconfs, tutorials, presentations):
            for (room, days) in collection.iteritems():
                for (day, ids) in days.iteritems():
                    if type(ids) is int:
                        ids = '(' + str(ids) + ')' # fix for single tuple
                    sql_execute("UPDATE proposal SET theatre = '%s', scheduled = '%s', accepted = TRUE WHERE id IN %s" % (room, timestamp[day], str(ids)))
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
        work from there... [Invoicing] """
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
                    WHERE invoice_item.product_id = 28 AND invoice.void = NULL"""
        return sql_response(query)

    def accom_uni_registers(self):
        """ People who selected any form as university accommodation. (Paid only) [Accommodation] """
        uni_list = self.dbsession.query(Product).filter(Product.description.like('University Accommodation %')).all()
        c.columns = ['Room Type', 'Name', 'e-mail', 'Checkin', 'Checkout']
        c.data = []
        for item in uni_list:
            for invoice_item in item.invoice_items:
                if invoice_item.invoice.paid() and not invoice_item.invoice.is_void():
                    c.data.append([item.description, 
                                   invoice_item.invoice.person.firstname + " " + invoice_item.invoice.person.lastname, 
                                   invoice_item.invoice.person.email_address, 
                                   invoice_item.invoice.person.registration.checkin,
                                   invoice_item.invoice.person.registration.checkout
                                 ])
        return render_response('admin/table.myt')

    def speakers_partners(self):
        """ Listing of speakers and their partner details [Speakers] """
        c.columns = ['Speaker', 'e-mail', 'Partner Programme', 'Penguin Dinner']
        c.data = []
        
        total_partners = 0
        total_dinner = 0
        speakers_count = 0
        for person in self.dbsession.query(Person).all():
            partners = []
            dinner_tickets = 0
            if person.is_speaker():
                for invoice in person.invoices:
                    for item in invoice.items:
                        if item.description.startswith("Partners Programme"):
                            partners.append(item.description + " x" + str(item.qty))
                            total_partners += item.qty
                        if item.description.startswith("Dinner"):
                            dinner_tickets += item.qty
                            total_dinner += item.qty
                c.data.append([person.firstname + " " + person.lastname,
                               person.email_address,
                               ", ".join(partners),
                               str(dinner_tickets)])
                speakers_count += 1
        c.data.append(['TOTALS:', str(speakers_count) + ' speakers', str(total_partners) + ' partners', str(total_dinner) + ' dinner tickets'])
        return render_response('admin/table.myt')

    def talks(self):
        """ List of talks for use in programme printing [Schedule] """
        c.text = "Talks with multiple speakers will appear twice."
        query = """SELECT proposal_type.name AS type, proposal.scheduled, proposal.title, proposal.abstract, person.firstname || ' ' || person.lastname as speaker, person.bio
                    FROM proposal
                    LEFT JOIN person_proposal_map ON (person_proposal_map.proposal_id = proposal.id)
                    LEFT JOIN person ON (person_proposal_map.person_id = person.id)
                    LEFT JOIN proposal_type ON (proposal_type.id = proposal.proposal_type_id)
                    WHERE proposal.accepted = True  
                    ORDER BY proposal_type.name, proposal.scheduled, proposal.title      
        """
        return sql_response(query)

    def zookeepr_sales(self):
        """ List of products and qty sold. [Inventory] """
        item_list = self.dbsession.query(InvoiceItem).all()
        total = 0
        c.columns = ['Item', 'Price', 'Qty', 'Amount']
        c.data = []
        for item in item_list:
            if item.invoice.paid() and not item.invoice.is_void():
                c.data.append([item.description, h.number_to_currency(item.cost/100), item.qty, h.number_to_currency(item.total()/100)])
                total += item.total()
        c.data.append(['','','Total:', h.number_to_currency(total/100)])
        return render_response('admin/table.myt')

    def partners_programme(self):
        """ List of partners programme contacts [Partners Programme] """
        partners_list = self.dbsession.query(Product).filter(Product.description.like('Partners Programme%')).all()
        c.text = "*Checkin and checkout dates aren't an accurate source."
        c.columns = ['Partner Type', 'Registration Name', 'Registration e-mail', 'Partners e-mail', 'Checkin*', 'Checkout*']
        c.data = []
        for item in partners_list:
            for invoice_item in item.invoice_items:
                if invoice_item.invoice.paid() and not invoice_item.invoice.is_void():
                    c.data.append([item.description, 
                                   invoice_item.invoice.person.firstname + " " + invoice_item.invoice.person.lastname, 
                                   invoice_item.invoice.person.email_address, 
                                   invoice_item.invoice.person.registration.partner_email, 
                                   invoice_item.invoice.person.registration.checkin,
                                   invoice_item.invoice.person.registration.checkout
                                 ])
        return render_response('admin/table.myt')
        
    def planet_lca(self):
        """ List of blog RSS feeds, planet compatible. [Mailing Lists] """
        c.text = """<p>List of RSS feeds for LCA planet.</p>
        <p><textarea cols="100" rows="25">"""
        
        count = 0
        for r in self.dbsession.query(Registration).filter(Registration.planetfeed != '').all():
            p = r.person
            c.text += "[" + r.planetfeed + "] name = " + p.firstname + " " + p.lastname + "\n"
            count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return render_response('admin/text.myt')

    def nonregistered(self):
        """ List of people with accounts on the website but who haven't started the registration process for the conference [Accounts] """
        
        sql = """SELECT registration.person_id FROM registration"""
        
        import zookeepr.model
        res = zookeepr.model.metadata.bind.execute(sql)
        data = res.fetchall()
        registration_ids = ", ".join([str(row[0]) for row in data])
                
        query = """SELECT person.firstname || ' ' || person.lastname as name, person.email_address
                    FROM person
                    WHERE person.id NOT IN(%s)
        """ % (registration_ids)
        return sql_response(query)

    def keysigning_participants_list(self):
        """ Generate a list of all current key id's [Keysigning] """
        from pylons import response
        response.headers['Content-type'] = 'text/plain'
        for keyid in self.keysigning_participants():
            response.content.append(keyid + "\n")

    def keysigning_single(self):
        """ Generate an A4 page of key fingerprints given a keyid [Keysigning] """
        if request.POST:
            keyid = request.POST['keyid']
            from pylons import response
            response.headers['Content-type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = ('attachment; filename=%s.pdf' %  keyid)
            pdf = keysigning_pdf(keyid)
            pdf_f = file(pdf)
            response.content = pdf_f.read()
            pdf_f.close()
        else:
            return render_response('admin/keysigning_single.myt')

    def keysigning_conference(self):
        """ Generate an A4 page of key fingerprints for everyone who has provided their fingerprint [Keysigning] """
        import os, tempfile
        (pdf_fd, pdf) = tempfile.mkstemp('.pdf')
        input_pdf = list()
        for keyid in self.keysigning_participants():
            input_pdf.append(keysigning_pdf(keyid))
        os.system('gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=' + pdf + ' -dBATCH ' + ' '.join(input_pdf))
        from pylons import response
        response.headers['Content-type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = ('attachment; filename=conference.pdf')
        pdf_f = file(pdf)
        response.content = pdf_f.read()
        pdf_f.close()

    def keysigning_participants(self):
        registration_list = self.dbsession.query(Registration).join('person').filter(Registration.keyid != None).filter(Registration.keyid != '').order_by(Person.lastname).all()
        key_list = list()
        for registration in registration_list:
            if registration.person.paid():
                key_list.append(registration.keyid)
        return key_list
        
    def rego_desk_list(self):
        """ List of people who have not checked in (see checkins table). [Registrations] """
        import zookeepr.model
        checkedin = zookeepr.model.metadata.bind.execute("SELECT person_id FROM checkins WHERE conference IS NOT NULL");
        checkedin_list = checkedin.fetchall()
        registration_list = self.dbsession.query(Registration).all()
        c.columns = ['ID', 'Name', 'Type', 'Shirts', 'Dinner Tickets', 'Partners Programme']
        c.data = []
        for registration in registration_list:
            if (registration.person.id not in [id[0] for id in checkedin_list]) and registration.person.paid():
                shirts = []
                dinner_tickets = 0
                ticket_types = []
                partners_programme = []
                for invoice in registration.person.invoices:
                    if invoice.paid() and not invoice.is_void():
                        for item in invoice.items:
                            if item.description.lower().startswith("discount"):
                                pass
                            elif item.description.lower().find("shirt") > -1:
                                shirts.append(item.description + " x" + str(item.qty))
                            elif item.description.lower().startswith("dinner"):
                                dinner_tickets += item.qty
                            elif item.description.lower().startswith("partners"):
                                partners_programme.append(item.description + " x" + str(item.qty))
                            elif item.description.lower().endswith("ticket") or item.description.lower().startswith("press pass"):
                                ticket_types.append(item.description + " x" + str(item.qty))
                c.data.append([registration.person.id,
                               registration.person.firstname + " " + registration.person.lastname,
                               ", ".join(ticket_types),
                               ", ".join(shirts),
                               dinner_tickets,
                               ", ".join(partners_programme)])

        return render_response('admin/table.myt')
        
    def miniconf_preferences(self):
        """ Preferred miniconfs. All people - including unpaid [Statistics] """
        registration_list = self.dbsession.query(Registration).all()
        c.columns = ['miniconf', 'People']
        c.data = []
        miniconfs = {}
        for registration in registration_list:
            if type(registration.miniconf) == list:
                for miniconf in registration.miniconf:
                    if miniconfs.has_key(miniconf):
                        miniconfs[miniconf] += 1
                    else:
                        miniconfs[miniconf] = 1
        for (miniconf, value) in miniconfs.iteritems():
            c.data.append([miniconf, value])

        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )

        return render_response('admin/table.myt')

    def previous_years_stats(self):
        """ Details on how many people have come to previous years of LCA. All people - including unpaid [Statistics] """
        registration_list = self.dbsession.query(Registration).all()
        c.columns = ['year', 'People']
        c.data = []
        years = {}
        veterans = []
        veterans_lca = []
        for registration in registration_list:
            if type(registration.prevlca) == list:
                for year in registration.prevlca:
                    if years.has_key(year):
                        years[year] += 1
                    else:
                        years[year] = 1
                if len(registration.prevlca) == len(lca_rego['past_confs']):
                    veterans.append(registration.person.firstname + " " + registration.person.lastname)
                elif len(registration.prevlca) == (len(lca_rego['past_confs']) - 1):
                    veterans_lca.append(registration.person.firstname + " " + registration.person.lastname)
        for (year, value) in years.iteritems():
            c.data.append([year, value])

        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s"><br />
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        c.text += "Veterans: " + ", ".join(veterans) + "<br><br>Veterans of LCA (excluding CALU): " + ", ".join(veterans_lca)
        return render_response('admin/table.myt')

    def acc_papers_xml(self):
        """ An XML file with titles and speakers of accepted talks, for use
        in AV splash screens [AV] """
        c.talks = self.dbsession.query(Proposal).filter_by(accepted=True).all()

        res = Response(render('admin/acc_papers_xml.myt', fragment=True))
        res.headers['Content-type']='text/plain; charset=utf-8'
        return res

    def people_by_country(self):
        """ Registered and paid people by country [Statistics] """
        data = {}
        for registration in self.dbsession.query(Registration).all():
            if registration.person.paid():
                country = registration.person.country.capitalize()
                data[country] = data.get(country, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return render_response('admin/table.myt')
     
    def people_by_state(self):
        """ Registered and paid people by state - Australia Only [Statistics] """
        data = {}
        for registration in self.dbsession.query(Registration).all():
            if registration.person.paid() and registration.person.country == "Australia":
                state = registration.person.state.capitalize()
                data[state] = data.get(state, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return render_response('admin/table.myt')
     
    def favourite_distro(self):
        """ Statistics on favourite distros. All people - including unpaid [Statistics] """
        data = {}
        for registration in self.dbsession.query(Registration).all():
            distro = registration.distro.capitalize()
            data[distro] = data.get(distro, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return render_response('admin/table.myt')
            
    def favourite_editor(self):
        """ Statistics on favourite editors. All people - including unpaid [Statistics] """
        data = {}
        for registration in self.dbsession.query(Registration).all():
            editor = registration.editor.capitalize()
            data[editor] = data.get(editor, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return render_response('admin/table.myt')
        
    def favourite_shell(self):
        """ Statistics on favourite shells. All people - including unpaid [Statistics] """
        data = {}
        for registration in self.dbsession.query(Registration).all():
            shell = registration.shell.capitalize()
            data[shell] = data.get(shell, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return render_response('admin/table.myt')

def keysigning_pdf(keyid):
    import os, tempfile, subprocess
    max_length = 66
    (txt_fd, txt) = tempfile.mkstemp('.txt')
    (pdf_fd, pdf) = tempfile.mkstemp('.pdf')
    os.system('gpg --recv-keys --keyserver keys.keysigning.org ' + keyid)
    fingerprint = subprocess.Popen(['gpg', '--fingerprint', keyid], stdout=subprocess.PIPE).communicate()[0]
    fingerprint_length = len(fingerprint.splitlines())
    if fingerprint_length > 0:
        fingerprint_num = max_length / int(fingerprint_length)
    else:
        fingerprint_num = 0
    for i in range(0,fingerprint_num):
        os.system('gpg --fingerprint %s >> %s' % (keyid, txt))
    os.system('mpage -1 -W `wc -L < %s` %s | ps2pdf - %s' % (txt, txt, pdf))
    os.close(pdf_fd);
    os.close(txt_fd);

    return pdf

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
