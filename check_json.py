#! /usr/bin/env python

"""
Nagios plugin to check a value returned from a uri in json format.

Copyright (c) 2009 Peter Kropf. All rights reserved.

Example:

Compare the "hostname" field in the json structure returned from
http://store.example.com/hostname.py against a known value.

    ./check_json hostname buenosaires http://store.example.com/hostname.py
"""


import urllib2
import simplejson
import sys
from optparse import OptionParser

prefix = 'JSON'

class nagios:
    ok       = (0, 'OK')
    warning  = (1, 'WARNING')
    critical = (2, 'CRITICAL')
    unknown  = (3, 'UNKNOWN')


def exit(status, message):
    print prefix + ' ' + status[1] + ' - ' + message
    sys.exit(status[0])


parser = OptionParser(usage='usage: %prog field_name expected_value uri')
options, args = parser.parse_args()


if len(sys.argv) < 3:
    exit(nagios.unknown, 'missing command line arguments')

field = args[0]
value = args[1]
uri = args[2]

try:
    j = simplejson.load(urllib2.urlopen(uri))
except urllib2.HTTPError, ex:
    exit(nagios.unknown, 'invalid uri')

if field not in j:
    exit(nagios.unknown, 'field: ' + field + ' not present')

if j[field] != value:
    exit(nagios.critical, j[field] + ' != ' + value)

exit(nagios.ok, j[field] + ' == ' + value)
