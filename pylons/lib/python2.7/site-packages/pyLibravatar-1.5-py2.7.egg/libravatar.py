"""
pyLibravatar Python module for Libravatar

Copyright (C) 2011 Francois Marier <francois@libravatar.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import DNS
import hashlib
import random
import re
import urllib
from urlparse import urlsplit, urlunsplit

BASE_URL = 'http://cdn.libravatar.org/avatar/'
SECURE_BASE_URL = 'https://seccdn.libravatar.org/avatar/'
SERVICE_BASE = '_avatars._tcp'
SECURE_SERVICE_BASE = '_avatars-sec._tcp'
MIN_AVATAR_SIZE = 1
MAX_AVATAR_SIZE = 512


def libravatar_url(email=None, openid=None, https=False,
                   default=None, size=None):
    """
    Return a URL to the appropriate avatar
    """

    avatar_hash, domain = parse_user_identity(email, openid)
    query_string = parse_options(default, size)

    delegation_server = lookup_avatar_server(domain, https)
    return compose_avatar_url(delegation_server, avatar_hash,
                              query_string, https)


def parse_options(default, size):
    """
    Turn optional parameters into a query string.
    """

    query_string = ''
    if default:
        query_string = '?d=%s' % urllib.quote_plus(str(default))
    if size:
        try:
            size = int(size)
        except ValueError:
            return query_string  # invalid size, skip

        if len(query_string) > 0:
            query_string += '&'
        else:
            query_string = '?'
        query_string += 's=%s' % max(MIN_AVATAR_SIZE,
                                     min(MAX_AVATAR_SIZE, size))

    return query_string


def parse_user_identity(email, openid):
    """
    Generate user hash based on the email address or OpenID and return
    it along with the relevant domain.
    """

    hash_obj = None
    if email:
        lowercase_value = email.strip().lower()
        domain = lowercase_value.split('@')[-1]
        hash_obj = hashlib.new('md5')
    elif openid:
        # pylint: disable=E1103
        url = urlsplit(openid.strip())
        if url.username:
            password = url.password or ''
            netloc = url.username + ':' + password + '@' + url.hostname
        else:
            netloc = url.hostname
        lowercase_value = urlunsplit((url.scheme.lower(), netloc,
                                      url.path, url.query, url.fragment))
        domain = url.hostname
        hash_obj = hashlib.new('sha256')

    if not hash_obj:  # email and openid both missing
        return (None, None)

    hash_obj.update(lowercase_value)
    return (hash_obj.hexdigest(), domain)


def compose_avatar_url(delegation_server, avatar_hash, query_string, https):
    """
    Assemble the final avatar URL based on the provided components.
    """

    avatar_hash = avatar_hash or ''
    query_string = query_string or ''

    base_url = BASE_URL
    if https:
        base_url = SECURE_BASE_URL

    if delegation_server:
        if https:
            base_url = "https://%s/avatar/" % delegation_server
        else:
            base_url = "http://%s/avatar/" % delegation_server

    return base_url + avatar_hash + query_string


def service_name(domain, https):
    """
    Return the DNS service to query for a given domain and scheme.
    """

    if not domain:
        return None

    if https:
        return "%s.%s" % (SECURE_SERVICE_BASE, domain)
    else:
        return "%s.%s" % (SERVICE_BASE, domain)


def lookup_avatar_server(domain, https):
    """
    Extract the avatar server from an SRV record in the DNS zone

    The SRV records should look like this:

       _avatars._tcp.example.com.     IN SRV 0 0 80  avatars.example.com
       _avatars-sec._tcp.example.com. IN SRV 0 0 443 avatars.example.com
    """

    DNS.DiscoverNameServers()
    try:
        dns_request = DNS.Request(name=service_name(domain, https),
                                  qtype='SRV').req()
    except DNS.DNSError as message:
        print "DNS Error: %s" % message
        return None

    if 'NXDOMAIN' == dns_request.header['status']:
        # Not an error, but no point in going any further
        return None

    if dns_request.header['status'] != 'NOERROR':
        print "DNS Error: status=%s" % dns_request.header['status']
        return None

    records = []
    for answer in dns_request.answers:
        if (not 'data' in answer) or (not answer['data']):
            continue
        if (not answer['typename']) or (answer['typename'] != 'SRV'):
            continue

        srv_record = {'priority': int(answer['data'][0]),
                      'weight': int(answer['data'][1]),
                      'port': int(answer['data'][2]),
                      'target': answer['data'][3]}

        records.append(srv_record)

    return normalized_target(records, https)


def normalized_target(records, https):
    """
    Pick the right server to use and return its normalized hostname
    (i.e. only include the port number if it's necessary).
    """

    target, port = sanitize_target(srv_hostname(records))

    if target and ((https and port != 443) or (not https and port != 80)):
        return "%s:%s" % (target, port)

    return target


def sanitize_target(args):
    """
    Ensure we are getting a (mostly) valid hostname and port number
    from the DNS resolver.
    """
    target, port = args

    if not target or not port:
        return (None, None)

    if not re.match('^[0-9a-zA-Z\-.]+$', str(target)):
        return (None, None)

    try:
        if int(port) < 1 or int(port) > 65535:
            return (None, None)
    except ValueError:
        return (None, None)

    return (target, port)


def srv_hostname(records):
    """
    Return the right (target, port) pair from a list of SRV records.
    """

    if len(records) < 1:
        return (None, None)

    if 1 == len(records):
        srv_record = records[0]
        return (srv_record['target'], srv_record['port'])

    # Keep only the servers in the top priority
    priority_records = []
    total_weight = 0
    top_priority = records[0]['priority']  # highest priority = lowest number

    for srv_record in records:
        if srv_record['priority'] > top_priority:
            # ignore the record (srv_record has lower priority)
            continue
        elif srv_record['priority'] < top_priority:
            # reset the asrv_recorday (srv_record has higher priority)
            top_priority = srv_record['priority']
            total_weight = 0
            priority_records = []

        total_weight += srv_record['weight']

        if srv_record['weight'] > 0:
            priority_records.append((total_weight, srv_record))
        else:
            # zero-weigth elements must come first
            priority_records.insert(0, (0, srv_record))

    if 1 == len(priority_records):
        srv_record = priority_records[0][1]
        return (srv_record['target'], srv_record['port'])

    # Select first record according to RFC2782 weight
    # ordering algorithm (page 3)
    random_number = random.randint(0, total_weight)

    for record in priority_records:
        weighted_index, srv_record = record

        if weighted_index >= random_number:
            return (srv_record['target'], srv_record['port'])

    print 'There is something wrong with our SRV weight ordering algorithm'
    return (None, None)
