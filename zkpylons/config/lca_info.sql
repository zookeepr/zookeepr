DROP TABLE IF EXISTS config;

CREATE TABLE config (
	category TEXT,
 	key      TEXT,
 	value    JSON, -- Update type to JSONB with postgres >= 9.4
	description TEXT,
	PRIMARY KEY (category, key)
);

GRANT ALL ON config TO zookeepr;

-- All value is type JSON, all values must be valid JSON
INSERT INTO config (category, key, value, description) VALUES
('general', 'password_salt',               '"changeme"', 'Used to salt the has used to store user passwords. This should be changed to a random string when the site is initially set up to prevent rainbow table attacks. Changing this field will break every users password.'),
('general', 'password_iterations',         '"400000"', 'Used to configure PBKDF2 hash, this is not currently used but will be transitioned to in the future.'),
('general', 'paymentgateway_userid',       '""', 'As provided by PxPay.'),
('general', 'paymentgateway_secretkey',    '""', 'As provided by PxPay.'),
('general', 'contact_email',               '"contact@lca2011.linux.org.au"', 'General contact email address. Provided at several locations through the site and used as the outgoing email From address.'),
('general', 'bcc_email',                   '"archive@lca2011.linux.org.au"', 'All email sent by Zookeepr will be BCC to this address for storage.'),
('general', 'webmaster_email',             '"webmaster@lca2011.linux.org.au"', 'Provided on the site for error reports and login problems.'),
('general', 'event_parent_organisation',   '"Linux Australia"', ''),
('general', 'event_parent_url',            '"http://www.linux.org.au/"', ''),
('general', 'event_generic_name',          '"linux.conf.au"', ''),
('general', 'event_name',                  '"linux.conf.au 2011"', ''),
('general', 'event_shortname',             '"lca2011"', ''),
('general', 'event_city',                  '"Hobart"', ''),
('general', 'event_host',                  '"lca2011.linux.org.au"', ''),
('general', 'event_url',                   '"http://lca2011.linux.org.au"', ''),
('general', 'event_permalink',             '"http://lca2011.linux.org.au"', ''),
('general', 'event_hashtag',               '"#LCA2011"', 'Used for Facebook and Twitter.'),
('general', 'event_tax_number',            '"ABN 56 987 117 479"', ''),
('general', 'event_postal_address',        '"PO BOX 2010 Keperra, Queensland, 4054"', ''),
('general', 'event_fax_number',            '""', 'Optional, provided on invoices if set. Should be an international phone number.'),
('general', 'event_phone_number',          '"+61 7 3103 7998"', 'Optional, provided on invoices if set. Should be an international phone number.'),
('general', 'event_byline',                '"linux.conf.au 2011 | 24 - 29 Jan | Follow the Flow"', ''),
('general', 'event_pricing_disclaimer',    '"All prices are in Australian dollars and include 10% GST."', ''),
('general', 'event_trademark_notice',      '"Linux is a registered trademark of Linus Torvalds"', ''),
('general', 'event_airport_code',          '"BNE"', ''),
('general', 'media_license_name',          '"Creative Commons Attribution-Share Alike License"', ''),
('general', 'media_license_url' ,          '"http://creativecommons.org/licenses/by-sa/3.0/"', ''),
('general', 'sales_tax_multiplier',        '""', 'Used to calculate the sales tax portion of the amount of money in an invoice. tax = amount * sales_tax_multiplier. Only one of sales_tax_multiplier or sales_tax_divisor should be set.'),
('general', 'sales_tax_divisor',           '"11"', 'Used to calculate the sales tax portion of the amount of money in an invoice. tax = amount / sales_tax_divisor. Only one of sales_tax_multiplier or sales_tax_divisor should be set.'),
('general', 'invoice_message',             '"To qualify for the earlybird discount you must have registered and paid by the 8th of November (unless earlybird tickets sell out earlier)."', 'Optional notice to appear above the invoice statement. Set this to blank to disable.'),
('general', 'cfp_status',                  '"closed"', 'State of the call for papers process. Should be either "not_open", "open" or "closed". Not open is used before the process, closed afterwards.'),
('general', 'cfmini_status',               '"closed"', 'State of the call for miniconfs process. Should be either "not_open", "open" or "closed". Not open is used before the process, closed afterwards.'),
('general', 'proposal_editing',            '"open"', 'Allows editing of CFP proposals, state should typically mirror cfp_status.'),
('general', 'funding_status',              '"not_open"', 'State of the funding process. Should be either "not_open", "open" or "closed". Not open is used before the process, closed afterwards.'),
('general', 'funding_editing',             '"not_open"', 'Allows editing of funding proposals, state should typically mirror funding_status.'),
('general', 'conference_status',           '"open"', 'State of the conference registration process. Should be either "debug", "not_open", "open" or "closed".'),
('general', 'account_creation',            '"True"', 'Toggle to allow account creation. Should be either "True" or "False".'),
('general', 'cfp_hide_assistance_info',    '"no"', 'Toggles hiding assistance requests in the proposal submission acknowledgement. Should be either "no" or "yes".'),
('general', 'cfp_hide_assistance_options', '"no"', 'Toggles hiding assistance requests in the proposal form. Should be either "no", "yes" or "by_email". By email will prompt them to reach out on the contact email.'),
('general', 'cfp_hide_scores',             '"no"', 'Allows hiding of proposal scores to other reviewers. Should be either "no" or "yes".'),
('general', 'proposal_update_email',       '"archive@lca2011.linux.org.au"', 'An email is sent to this address every time a proposal is edited. Can be set to blank to disable the functionality.'),
('general', 'google_map_url',              '"http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=117014168848232117270.00048b169407c904d6506"', ''),
('general', 'google_map_latlng',           '"-27.478216,153.019466"', ''),
('general', 'mailing_list_announce_url',   '"http://lists.linux.org.au/listinfo/lca-announce"', ''),
('general', 'mailing_list_announce_addr',  '"lca-announce@linux.org.au"', ''),
('general', 'mailing_list_chat_url',       '"http://lists.lca2011.linux.org.au/lca2011-chat"', ''),
('general', 'mailing_list_chat_addr',      '"lca2011-chat@lists.lca2011.linux.org.au"', ''),
('general', 'date',                        '"2011-01-24T09:00:00"', 'Date of the start of the conference. Must be in the format yyyy-mm-ddThh:mm:ss.'),
('general', 'time_zone',                   '"Australia/Melbourne"', 'Timezone of the conference. Should be a valid pytz timezone.'),
('general', 'cfp_miniconf_list', '["(none)", "Sysadmin", "Business", "Haecksen"]', 'List of miniconfs that reviewers can recommend a talk be used for. Must be a JSON list of strings.'),
('general', 'sponsors', '
	{
		"top": [
			{"alt": "lca2007", "src": "/images/history/lca2007-logo.png", "href": "http://lca2007.linux.org.au/"},
			{"alt": "lca2006", "src": "/images/history/lca2006-logo.png", "href": "http://lca2006.linux.org.au/"}
		],
		"slideshow": [
			{"alt": "lca2008", "src": "/images/history/lca2008-logo.png", "href": "http://lca2008.linux.org.au/"},
			{"alt": "lca2009", "src": "/images/history/lca2009-logo.png", "href": "http://lca2009.linux.org.au/"}
		]
	}
', 'Used to control the sidebar sponsors ad display. The value must be a JSON object with two optional keys, "top" and "slideshow". Top is used for the emperor sponsors which are permanently displayed, slideshow is used for the other sponsors which are cycled through. Each of "top" and "slideshow" contain an array of objects. Each object must define "alt", "src" and "href", these are used as parameters to <a> and <img> tags.');

INSERT INTO config (category, key, value, description) VALUES
('rego', 'personal_info', '{
	"phone" : "yes",
	"home_address" : "yes"
}', 'Allows toggling collecting personal info (phone number and address) during the registration and sign up process. Value must be a JSON object with two keys, "phone" and "home_address". Each of "phone" and "home_address" must have the value "yes" or "no". If disabled the user will not be prompted.'),
('rego', 'pgp_collection', '"yes"', 'Toggles prompt for PGP key during registration.'),
('rego', 'confirm_email_address', '"yes"', 'Require an email address confirmation during sign up. Must be "yes" or "no".'),
('rego', 'ask_past_confs', '"yes"', 'Toggles prompt for information on prior conferences during registration. Must be "yes" or "no".'),
('rego', 'lca_optional_stuff', '"yes"', 'Toggles prompt for shell, editor, distro etc. during registration. Must be "yes" or "no".'),
('rego', 'volunteer', '[
	{"title": "Volunteer Category", "questions": [
		{"name": "Student Volunteer", "description": "I am eligible to attend as a Student and am willing to donate 100% of my time to the conference. I understand that I will be able to attend for free."},
		{"name": "Hobbyist Volunteer", "description": "I am eligible to attend as a Hobbyist and am willing to donate at least 50% of my time to the conference. I understand that I will be able to attend for the price of a student admission. (If you are happy to donate more than 50% of your time, please indicate a percentage in the \"Other:\" section.)"},
		{"name": "Other Volunteer", "description": "I do not fit into the categories above or want to volunteer for a specific project or for less than the percentages above. Please provide details in the \"Other:\" section."}
	]},
	{"title": "Availability", "questions": [
		{"name": "Setup", "description": "I am available on the weekend prior to the conference (22 - 23 January) to help with setup."},
		{"name": "Sunday Registrations", "description": "I am available on the afternoon of Sunday 23 January to assist with pre-conference registrations."},
		{"name": "Conference", "description": "I am available for the full week of the conference (24 - 28 January)."},
		{"name": "Pack up", "description": "I am available on the evening of Friday 28 January and Saturday 29 January to pack-up the conference."},
		{"name": "Other Dates", "description": "Please provide details in the \"Other:\" section."}
	]},
	{"title": "I am able and willing to help with ...", "questions": [
		{"name": "Speaker Introductions", "description": "Leading A/V and Ushers in a room, introducing speakers, keeping them to schedule, public announcements, etc."},
		{"name": "A/V", "description": "Filming in a lecture theatre. Training will be provided."},
		{"name": "Usher", "description": "Helping manage rooms, get people to seats, etc."},
		{"name": "Registration Desk", "description": "Sign people into the conference and help with general enquiries."},
		{"name": "Venue Helper", "description": "Help with setting up break times, tables and chairs, and other miscellaneous things."},
		{"name": "Other", "description": "Please provide details in the \"Other:\" section."}
	]}
]', 'This value defines questions which will be asked of volunteers. Questions are categorised and presented as a series of checkboxes. The value is a JSON array, each member of which is an object representing a group of questions. Each group object must have a "title" key containing a string and a questions key with another array. The questions array is a series of objects with the key "name" and "description", both values should be strings.'),
('rego', 'shells', '["bash", "busybox", "csh", "dash", "emacs", "ksh", "sh", "smrsh", "tcsh", "XTree Gold", "zsh"]', 'JSON array of shells that the user can choose from during registration.'),
('rego', 'editors', '["bluefish", "eclipse", "emacs", "gedit", "jed", "kate", "nano", "vi", "vim", "xemacs"]', 'JSON array of editors that the user can choose from during registration.'),
('rego', 'distros', '["Arch", "Arch/Hurd", "CentOS", "Darwin", "Debian", "Fedora", "FreeBSD", "FreeDOS", "Gentoo", "Hurd", "GNU Emacs","Haiku OS","kFreeBSD","L4", "Mandriva", "Minix", "MeeGo", "NetBSD", "Nexenta", "OpenBSD", "OpenSolaris", "OpenSuSE", "SLES","Oracle Enterprise Linux", "RHEL", "Slackware", "Ubuntu", "Xandros"]', 'JSON array of distributions that the user can choose from during registration.'),
('rego', 'vcses', '[".bak", "arch", "bazaar", "bitkeeper", "cvs", "darcs", "git", "mercurial", "monotone", "perforce", "rcs", "sourcesafe", "subversion"]', 'JSON array of version control systems that the user can choose from during registration.'),
('rego', 'past_confs', '[
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
	["12", "2012 (Ballarat)"]
]', 'List of past conferences the user can choose from. The value is a JSON array where each value is another array. The inner array must have two values, an id such as the year and the human readable name.'),
('rego', 'silly_description', '{
	"starts" : ["a", "a", "a", "one", "no"],
	"adverbs" : ["strongly",
			"poorly", "badly", "well", "dynamically",
			"hastily", "statically", "mysteriously",
			"buggily", "extremely", "nicely", "strangely",
			"irritatingly", "unquestionably", "clearly",
			"plainly", "silently", "abstractly", "validly",
			"invalidly", "immutably", "oddly", "disturbingly",
			"atonally", "randomly", "amusingly", "widely",
			"narrowly", "manually", "automatically", "audibly",
			"brilliantly", "independently", "definitively",
			"provably", "improbably", "distortingly",
			"confusingly", "decidedly", "historically",
			"shiny", "troublesome"],
	"adjectives" : ["invalid", "valid",
			"referenced", "dereferenced", "unreferenced",
			"illegal", "legal",
			"questionable",
			"alternate", "implemented", "unimplemented",
			"terminal", "non-terminal",
			"static", "dynamic",
			"qualified", "unqualified",
			"constant", "variable",
			"volatile", "non-volatile",
			"abstract", "concrete",
			"fungible", "non-fungible",
			"untyped", "variable",
			"mutable", "immutable",
			"sizable", "minuscule",
			"perverse", "immovable",
			"compressed", "uncompressed",
			"surreal", "allegorical",
			"trivial", "nontrivial"],
	"nouns" : ["pointer", "structure",
			"definition", "declaration", "type", "union",
			"coder", "admin", "hacker", "kitten", "mistake",
			"conversion", "implementation", "design", "analysis",
			"neophyte", "expert", "bundle", "package",
			"abstraction", "theorem", "display", "distro",
			"restriction", "device", "function", "reference",
			"alien"]
}', 'Input to the silly description generator. The value is a JSON object with four keys, "starts", "adverbs", "adjectives" and "nouns". Each of these has a value which is an array of strings. The generator takes one element from each array to piece together the string.');
