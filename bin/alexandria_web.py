#!/usr/bin/env python2.7

import sys
import os
try:
    import alexandria
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import alexandria

import alexandria.web.api
import web

mapping = (
    "/api", alexandria.web.api.app
)

app = web.subdir_application(mapping)

if __name__ == '__main__':
    app.run()
