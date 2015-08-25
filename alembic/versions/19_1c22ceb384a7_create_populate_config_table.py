"""create & populate config table

Revision ID: 1c22ceb384a7
Revises: 4ed1a2dd2573
Create Date: 2015-08-12 23:15:45.242942

"""

# revision identifiers, used by Alembic.
revision = '1c22ceb384a7'
down_revision = '3b5c7d3c8366'

from alembic import op
import sqlalchemy as sa

# For exporting data on downgrade
import pprint

# For random salt generation & password updateing
import os
import hashlib

# Import existing values, if they exist
try:
    temp = __import__('zkpylons.config.lca_info', fromlist= ['lca_info', 'lca_rego'])
    info = getattr(temp, 'lca_info', {})
    rego = getattr(temp, 'lca_rego', {})
except:
    info = {}
    rego = {}

# Default data set
data = [
    {
        'category'    : 'general',
        'key'         : 'password_salt',
        'value'       : hashlib.sha256(os.urandom(32)).hexdigest(),
        'description' : 'Used to salt the has used to store user passwords. This should be changed to a random string when the site is initially set up to prevent rainbow table attacks. Changing this field will break every users password.'
    },
    {
        'category'    : 'general',
        'key'         : 'password_iterations',
        'value'       : '400000',
        'description' : 'Used to configure PBKDF2 hash, this is not currently used but will be transitioned to in the future.'
    },
    {
        'category'    : 'general',
        'key'         : 'paymentgateway_userid',
        'value'       : '',
        'description' : 'As provided by PxPay.'
    },
    {
        'category'    : 'general',
        'key'         : 'paymentgateway_secretkey',
        'value'       : '',
        'description' : 'As provided by PxPay.'
},
    {
        'category'    : 'general',
        'key'         : 'contact_email',
        'value'       : 'contact@lca2011.linux.org.au',
        'description' : 'General contact email address. Provided at several locations through the site and used as the outgoing email From address.'
},
    {
        'category'    : 'general',
        'key'         : 'bcc_email',
        'value'       : 'archive@lca2011.linux.org.au',
        'description' : 'All email sent by Zookeepr will be BCC to this address for storage.'
},
    {
        'category'    : 'general',
        'key'         : 'webmaster_email',
        'value'       : 'webmaster@lca2011.linux.org.au',
        'description' : 'Provided on the site for error reports and login problems.'
},
    {
        'category'    : 'general',
        'key'         : 'event_parent_organisation',
        'value'       : 'Linux Australia',
        'description' : ''
},
    {
        'category'    : 'general',
        'key'         : 'event_parent_url',
        'value'       : 'http://www.linux.org.au/',
        'description' : ''
},
    {
        'category'    : 'general',
        'key'         : 'event_generic_name',
        'value'       : 'linux.conf.au',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_name',
        'value'       : 'linux.conf.au 2011',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_shortname',
        'value'       : 'lca2011',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_city',
        'value'       : 'Hobart',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_host',
        'value'       : 'lca2011.linux.org.au',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_url',
        'value'       : 'http://lca2011.linux.org.au',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_permalink',
        'value'       : 'http://lca2011.linux.org.au',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_hashtag',
        'value'       : '#LCA2011',
        'description' : 'Used for Facebook and Twitter.'
    },
    {
        'category'    : 'general',
        'key'         : 'event_tax_number',
        'value'       : 'ABN 56 987 117 479',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_postal_address',
        'value'       : 'PO BOX 2010 Keperra, Queensland, 4054',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_fax_number',
        'value'       : '',
        'description' : 'Optional, provided on invoices if set. Should be an international phone number.'
    },
    {
        'category'    : 'general',
        'key'         : 'event_phone_number',
        'value'       : '+61 7 3103 7998',
        'description' : 'Optional, provided on invoices if set. Should be an international phone number.'
    },
    {
        'category'    : 'general',
        'key'         : 'event_byline',
        'value'       : 'linux.conf.au 2011 | 24 - 29 Jan | Follow the Flow',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_pricing_disclaimer',
        'value'       : 'All prices are in Australian dollars and include 10% GST.',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_trademark_notice',
        'value'       : 'Linux is a registered trademark of Linus Torvalds',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'event_airport_code',
        'value'       : 'BNE',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'media_license_name',
        'value'       : 'Creative Commons Attribution-Share Alike License',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'media_license_url' ,
        'value'       : 'http://creativecommons.org/licenses/by-sa/3.0/',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'sales_tax_multiplier',
        'value'       : '',
        'description' : 'Used to calculate the sales tax portion of the amount of money in an invoice. tax = amount * sales_tax_multiplier. Only one of sales_tax_multiplier or sales_tax_divisor should be set.'
    },
    {
        'category'    : 'general',
        'key'         : 'sales_tax_divisor',
        'value'       : '11',
        'description' : 'Used to calculate the sales tax portion of the amount of money in an invoice. tax = amount / sales_tax_divisor. Only one of sales_tax_multiplier or sales_tax_divisor should be set.'
    },
    {
        'category'    : 'general',
        'key'         : 'invoice_message',
        'value'       : 'To qualify for the earlybird discount you must have registered and paid by the 8th of November (unless earlybird tickets sell out earlier).',
        'description' : 'Optional notice to appear above the invoice statement. Set this to blank to disable.'
    },
    {
        'category'    : 'general',
        'key'         : 'cfp_status',
        'value'       : 'closed',
        'description' : 'State of the call for papers process. Should be either "not_open", "open" or "closed". Not open is used before the process, closed afterwards.'
    },
    {
        'category'    : 'general',
        'key'         : 'cfmini_status',
        'value'       : 'closed',
        'description' : 'State of the call for miniconfs process. Should be either "not_open", "open" or "closed". Not open is used before the process, closed afterwards.'
    },
    {
        'category'    : 'general',
        'key'         : 'proposal_editing',
        'value'       : 'open',
        'description' : 'Allows editing of CFP proposals, state should typically mirror cfp_status.'
    },
    {
        'category'    : 'general',
        'key'         : 'funding_status',
        'value'       : 'not_open',
        'description' : 'State of the funding process. Should be either "not_open", "open" or "closed". Not open is used before the process, closed afterwards.'
    },
    {
        'category'    : 'general',
        'key'         : 'funding_editing',
        'value'       : 'not_open',
        'description' : 'Allows editing of funding proposals, state should typically mirror funding_status.'
    },
    {
        'category'    : 'general',
        'key'         : 'conference_status',
        'value'       : 'open',
        'description' : 'State of the conference registration process. Should be either "debug", "not_open", "open" or "closed".'
    },
    {
        'category'    : 'general',
        'key'         : 'account_creation',
        'value'       : 'True',
        'description' : 'Toggle to allow account creation. Should be either "True" or "False".'
    },
    {
        'category'    : 'general',
        'key'         : 'cfp_hide_assistance_info',
        'value'       : 'no',
        'description' : 'Toggles hiding assistance requests in the proposal submission acknowledgement. Should be either "no" or "yes".'
    },
    {
        'category'    : 'general',
        'key'         : 'cfp_hide_assistance_options',
        'value'       : 'no',
        'description' : 'Toggles hiding assistance requests in the proposal form. Should be either "no", "yes" or "by_email". By email will prompt them to reach out on the contact email.'
    },
    {
        'category'    : 'general',
        'key'         : 'cfp_hide_scores',
        'value'       : 'no',
        'description' : 'Allows hiding of proposal scores to other reviewers. Should be either "no" or "yes".'
    },
    {
        'category'    : 'general',
        'key'         : 'proposal_update_email',
        'value'       : 'archive@lca2011.linux.org.au',
        'description' : 'An email is sent to this address every time a proposal is edited. Can be set to blank to disable the functionality.'
    },
    {
        'category'    : 'general',
        'key'         : 'google_map_url',
        'value'       : 'http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=117014168848232117270.00048b169407c904d6506',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'google_map_latlng',
        'value'       : '-27.478216,153.019466',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'mailing_list_announce_url',
        'value'       : 'http://lists.linux.org.au/listinfo/lca-announce',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'mailing_list_announce_addr',
        'value'       : 'lca-announce@linux.org.au',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'mailing_list_chat_url',
        'value'       : 'http://lists.lca2011.linux.org.au/lca2011-chat',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'mailing_list_chat_addr',
        'value'       : 'lca2011-chat@lists.lca2011.linux.org.au',
        'description' : ''
    },
    {
        'category'    : 'general',
        'key'         : 'date',
        'value'       : '2011-01-24T09:00:00',
        'description' : 'Date of the start of the conference. Must be in the format yyyy-mm-ddThh:mm:ss.'
    },
    {
        'category'    : 'general',
        'key'         : 'time_zone',
        'value'       : 'Australia/Melbourne',
        'description' : 'Timezone of the conference. Should be a valid pytz timezone.'
    },
    {
        'category'    : 'general',
        'key'         : 'cfp_miniconf_list',
        'value'       : ["(none)", "Sysadmin", "Business", "Haecksen"],
        'description' : 'List of miniconfs that reviewers can recommend a talk be used for. Must be a JSON list of strings.'
    },
    {
        'category'    : 'general',
        'key'         : 'sponsors',
        'value'       : {
            "top" : [
                {
                    "alt"  : "lca2007",
                    "src"  : "/images/history/lca2007-logo.png",
                    "href" : "http://lca2007.linux.org.au/"
                },
                {
                    "alt"  : "lca2006",
                    "src"  : "/images/history/lca2006-logo.png",
                    "href" : "http://lca2006.linux.org.au/"
                }
            ],
            "slideshow" : [
                {
                    "alt"  : "lca2008",
                    "src"  : "/images/history/lca2008-logo.png",
                    "href" : "http://lca2008.linux.org.au/"
                },
                {
                    "alt"  : "lca2009",
                    "src"  : "/images/history/lca2009-logo.png",
                    "href" : "http://lca2009.linux.org.au/"
                }
            ]
        },
        'description' : 'Used to control the sidebar sponsors ad display. The value must be a JSON object with two optional keys, "top" and "slideshow". Top is used for the emperor sponsors which are permanently displayed, slideshow is used for the other sponsors which are cycled through. Each of "top" and "slideshow" contain an array of objects. Each object must define "alt", "src" and "href", these are used as parameters to <a> and <img> tags.'
    },
    {
        'category'    : 'rego',
        'key'         : 'personal_info',
        'value'       : {
            "phone"        : "yes",
            "home_address" : "yes"
        },
        'description' : 'Allows toggling collecting personal info (phone number and address) during the registration and sign up process. Value must be a JSON object with two keys, "phone" and "home_address". Each of "phone" and "home_address" must have the value "yes" or "no". If disabled the user will not be prompted.'
    },
    {
        'category'    : 'rego',
        'key'         : 'pgp_collection',
        'value'       : 'yes',
        'description' : 'Toggles prompt for PGP key during registration.'
    },
    {
        'category'    : 'rego',
        'key'         : 'confirm_email_address',
        'value'       : 'yes',
        'description' : 'Require an email address confirmation during sign up. Must be "yes" or "no".'
    },
    {
        'category'    : 'rego',
        'key'         : 'ask_past_confs',
        'value'       : 'yes',
        'description' : 'Toggles prompt for information on prior conferences during registration. Must be "yes" or "no".'
    },
    {
        'category'    : 'rego',
        'key'         : 'lca_optional_stuff',
        'value'       : 'yes',
        'description' : 'Toggles prompt for shell, editor, distro etc. during registration. Must be "yes" or "no".'
    },
    {
        'category'    : 'rego',
        'key'         : 'volunteer',
        'value'       : [
            {
                "title" : "Volunteer Category",
                "questions" : [
                    {
                        "name" : "Student Volunteer",
                        "description" : "I am eligible to attend as a Student and am willing to donate 100% of my time to the conference. I understand that I will be able to attend for free."
                    },
                    {
                        "name" : "Hobbyist Volunteer",
                        "description" : "I am eligible to attend as a Hobbyist and am willing to donate at least 50% of my time to the conference. I understand that I will be able to attend for the price of a student admission. (If you are happy to donate more than 50% of your time, please indicate a percentage in the \"Other :\" section.)"
                    },
                    {
                        "name" : "Other Volunteer",
                        "description" : "I do not fit into the categories above or want to volunteer for a specific project or for less than the percentages above. Please provide details in the \"Other:\" section."
                    }
                ]
            },
            {
                "title" : "Availability",
                "questions" : [
                    {
                        "name" : "Setup",
                        "description" : "I am available on the weekend prior to the conference (22 - 23 January) to help with setup."
                    },
                    {
                        "name" : "Sunday Registrations",
                        "description" : "I am available on the afternoon of Sunday 23 January to assist with pre-conference registrations."
                    },
                    {
                        "name" : "Conference",
                        "description" : "I am available for the full week of the conference (24 - 28 January)."
                    },
                    {
                        "name" : "Pack up",
                        "description" : "I am available on the evening of Friday 28 January and Saturday 29 January to pack-up the conference."
                    },
                    {
                        "name" : "Other Dates",
                        "description" : "Please provide details in the \"Other:\" section."
                    }
                ]
            },
            {
                "title" : "I am able and willing to help with ...",
                "questions" : [
                    {
                        "name" : "Speaker Introductions",
                        "description" : "Leading A/V and Ushers in a room, introducing speakers, keeping them to schedule, public announcements, etc."
                    },
                    {
                        "name" : "A/V",
                        "description" : "Filming in a lecture theatre. Training will be provided."
                    },
                    {
                        "name" : "Usher",
                        "description" : "Helping manage rooms, get people to seats, etc."
                    },
                    {
                        "name" : "Registration Desk",
                        "description" : "Sign people into the conference and help with general enquiries."
                    },
                    {
                        "name" : "Venue Helper",
                        "description" : "Help with setting up break times, tables and chairs, and other miscellaneous things."
                    },
                    {
                        "name" : "Other",
                        "description" : "Please provide details in the \"Other:\" section."
                    }
                ]
            }
        ],
        'description' : 'This value defines questions which will be asked of volunteers. Questions are categorised and presented as a series of checkboxes. The value is a JSON array, each member of which is an object representing a group of questions. Each group object must have a "title" key containing a string and a questions key with another array. The questions array is a series of objects with the key "name" and "description", both values should be strings.'
    },
    {
        'category'    : 'rego',
        'key'         : 'shells',
        'value'       : ["bash", "busybox", "csh", "dash", "emacs", "ksh", "sh", "smrsh", "tcsh", "XTree Gold", "zsh"],
        'description' : 'JSON array of shells that the user can choose from during registration.'
    },
    {
        'category'    : 'rego',
        'key'         : 'editors',
        'value'       : ["bluefish", "eclipse", "emacs", "gedit", "jed", "kate", "nano", "vi", "vim", "xemacs"],
        'description' : 'JSON array of editors that the user can choose from during registration.'
    },
    {
        'category'    : 'rego',
        'key'         : 'distros',
        'value'       : ["Arch", "Arch/Hurd", "CentOS", "Darwin", "Debian", "Fedora", "FreeBSD", "FreeDOS", "Gentoo", "Hurd", "GNU Emacs", "Haiku OS", "kFreeBSD", "Korora", "L4", "Mandriva", "Minix", "MeeGo", "NetBSD", "Nexenta", "OpenBSD", "OpenSolaris", "OpenSuSE", "SLES", "Oracle Enterprise Linux", "RHEL", "Slackware", "Ubuntu", "Xandros"],
        'description' : 'JSON array of distributions that the user can choose from during registration.'
    },
    {
        'category'    : 'rego',
        'key'         : 'vcses',
        'value'       : [".bak", "arch", "bazaar", "bitkeeper", "cvs", "darcs", "git", "mercurial", "monotone", "perforce", "rcs", "sourcesafe", "subversion"],
        'description' : 'JSON array of version control systems that the user can choose from during registration.'
    },
    {
        'category'    : 'rego',
        'key'         : 'past_confs',
        'value'       : [
            ["99", "1999 (CALU, Melbourne)"],
            ["01", "2001 (Sydney)"],
            ["02", "2002 (Brisbane)"],
            ["03", "2003 (Perth)"],
            ["04", "2004 (Adelaide)"],
            ["05", "2005 (Canberra)"],
            ["06", "2006 (Dunedin)"],
            ["07", "2007 (Sydney)"],
            ["08", "2008 (Melbourne)"],
            ["09", "2009 (Hobart)"],
            ["10", "2010 (Wellington)"],
            ["11", "2011 (Brisbane)"],
            ["12", "2012 (Ballarat)"],
            ["13", "2013 (Canberra)"],
            ["14", "2014 (Perth)"],
            ["15", "2015 (Auckland)"],
            ["16", "2016 (Geelong)"]
    ],
        'description' : 'List of past conferences the user can choose from. The value is a JSON array where each value is another array. The inner array must have two values, an id such as the year and the human readable name.'
    },
    {
        'category'    : 'rego',
        'key'         : 'silly_description',
        'value'       : {

            "starts"   : ["a", "a", "a", "one", "no"],
            "adverbs"  : [
                            "strongly", "poorly", "badly", "well", "dynamically", "hastily",
                            "statically", "mysteriously", "buggily", "extremely", "nicely",
                            "strangely", "irritatingly", "unquestionably", "clearly", "plainly",
                            "silently", "abstractly", "validly", "invalidly", "immutably",
                            "oddly", "disturbingly", "atonally", "randomly", "amusingly", "widely",
                            "narrowly", "manually", "automatically", "audibly", "brilliantly",
                            "independently", "definitively", "provably", "improbably", "distortingly",
                            "confusingly", "decidedly", "historically", "shiny", "troublesome"
                         ],
            "adjectives"  : [
                            "invalid", "valid", "referenced", "dereferenced", "unreferenced", "illegal",
                            "legal", "questionable", "alternate", "implemented", "unimplemented", "terminal",
                            "non-terminal", "static", "dynamic", "qualified", "unqualified", "constant",
                            "variable", "volatile", "non-volatile", "abstract", "concrete", "fungible",
                            "non-fungible", "untyped", "variable", "mutable", "immutable", "sizable",
                            "minuscule", "perverse", "immovable", "compressed", "uncompressed", "surreal",
                            "allegorical", "trivial", "nontrivial"
                            ],
            "nouns"  : [
                "pointer", "structure", "definition", "declaration", "type", "union", "coder",
                "admin", "hacker", "kitten", "mistake", "conversion", "implementation", "design",
                "analysis", "neophyte", "expert", "bundle", "package", "abstraction", "theorem",
                "display", "distro", "restriction", "device", "function", "reference", "alien"
            ]
    
        },
        'description' : 'Input to the silly description generator. The value is a JSON object with four keys, "starts", "adverbs", "adjectives" and "nouns". Each of these has a value which is an array of strings. The generator takes one element from each array to piece together the string.'
    }
]

def update_entry(entry, old_data, old_name):
    # Update data to use lca_info/rego types if they are set
    # Can't auto-convert complex types, like datetime objects
    temp = old_data.get(entry['key'])
    if type(temp).__name__ not in ['str', 'int', 'bool', 'list', 'dict', 'tuple', 'float', 'NoneType']:
        conversion_failures.append("%s['%s']" % (old_name, entry['key']))
        temp = None;
    if temp != None:
        entry['value'] = temp


# Update default data with current values, if set
conversion_failures = []
for e in data:
    if e['category'] == 'general':
        update_entry(e, info, 'lca_info')
    if e['category'] == 'rego':
        update_entry(e, rego, 'lca_rego')

def upgrade():

    config_table = op.create_table('config',
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('key', sa.Text(), nullable=False),
        sa.Column('value', sa.dialects.postgresql.JSON, nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('category', 'key')
    )

    try:
        __import__('zkpylons.config.lca_info') # Are we on an existing working install?
        print "MIGRATION NOTES"
        print "==============="
        print "This change has migrated your zkpylons/config/lca_info.py data in to the database."
        print "All your existing lca_info and lca_rego values have been imported, default values"
        print "have been restored for any missing portions."
        print ""
        print "The lca_menu and lca_submenus now live directly in your theme"
        print "You must set up the menus as you desire, it is not automatic."
        print ""
        print "The existing lca_info.py file is unchanged, but no longer used."
        print "Updating config values is now done at http://host/admin/change_config"
        print "Once you have verified that the import was successful lca_info.py can be deleted."
        if len(conversion_failures):
            print ""
            print "Note, the following values could not be converted automatically"
            for fail in conversion_failures:
                print "\t%s" % fail
    except:
        pass

    op.bulk_insert(config_table, data)

    if 'password_salt' not in 'info':
        # We don't have a preset salt to import from an existing configuration
        # So to avoid being insecure out of the box, we have generated one as a default value
        # The downside to this is that it has broken the default password
        # We restore the default and create a random password seed for extra protection

        default_pw = 'password'
        site_salt  = [x for x in data if x['key'] == 'password_salt'][0]['value']
        pw_salt    = hashlib.sha256(os.urandom(32)).hexdigest()
        enc_pw     = hashlib.sha256(default_pw + site_salt + pw_salt).hexdigest()

        op.execute("UPDATE person SET password_salt='%s', password_hash='%s' WHERE email_address='admin@zookeepr.org'" % (pw_salt, enc_pw))


def downgrade():
    # Export all the existing data to allow restoration of lca_info.py file
    dump = op.get_bind().execute("SELECT category, key, value FROM config").fetchall();

    # Build two hashes, lca_info and lca_rego
    lca_info = {}
    lca_rego = {}
    for e in dump:
        if e[0] == 'general':
            lca_info[e[1]] = e[2];
        if e[0] == 'rego':
            lca_rego[e[1]] = e[2];

    def de_unicode(object, context, maxlevels, level):
        if pprint._type(object) is unicode: object = str(object)
        return pprint._safe_repr(object, context, maxlevels, level)

    f = open('lca_info.py.downgrade', 'w')

    printer = pprint.PrettyPrinter(indent=2, stream=f)
    printer.format = de_unicode

    f.write('lca_info = ')
    printer.pprint(lca_info)
    f.write('lca_rego = ')
    printer.pprint(lca_rego)

    op.drop_table('config')

    print "MIGRATION NOTES"
    print "==============="
    print "Prior revisions stored the site configuration variables in zkpylons/config/lca_info.py"
    print ""
    print "The configuration data, which would otherwise be lost in this downgrade, has been"
    print "exported to lca_info.py.downgrade in your current working directory."
    print ""
    print "You should check this file and combine it with any menu items in your theme to generate"
    print "your lca_info.py for use going forward."
