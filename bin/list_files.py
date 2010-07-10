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
    for file in alexandria.discover.list_files(sys.argv[1], sys.argv[2]):
        print file

except IndexError:
    print "Usage: %s <host> <share>" % sys.argv[0]
