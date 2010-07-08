#!/usr/bin/env python

import os
import sys
try:
    import smbsearch
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import smbsearch

import smbsearch.discover
try:
    hosts = smbsearch.discover.list_hosts(sys.argv[1])
    for host in hosts:
        print "%s -> %s" % (host.address, host.hostname)
except IndexError:
    print "Usage: %s <workgroup>" % sys.argv[0]
