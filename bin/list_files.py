#!/usr/bin/env python

import os
import sys
try:
    import smbsearch
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import smbsearch

import smbsearch.share

try:
    smbsearch.share.list_files(sys.argv[1], sys.argv[2])
except IndexError:
    print "Usage: %s <host> <share>" % sys.argv[0]
