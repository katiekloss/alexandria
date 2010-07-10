#!/usr/bin/env python

import os
import sys
try:
    import alexandria
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import alexandria

import alexandria.discover
try:
    shares = alexandria.discover.list_shares(sys.argv[1])
    for share in shares:
        print share.name + ": " + share.comment
except IndexError:
    print "Usage: %s <host>" % sys.argv[0]
