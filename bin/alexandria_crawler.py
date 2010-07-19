#!/usr/bin/env python2.7

import os
import sys
import signal

try:
    import alexandria
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import alexandria

import logging
import alexandria.discover
import alexandria.crawler

crawler = None
logger = logging.getLogger('main')

def setupLogging(log_level):
    """Initializes the Python logging module."""
    logging.basicConfig(filename='crawler.log', level=log_level,
        format='%(asctime)s - %(module)s:%(funcName)s(%(lineno)d):%(levelname)s - %(message)s')

def main():
    """Run a crawler"""
    global crawler
    crawler = alexandria.crawler.Crawler()
    crawler.run()

def handleSigint(signal, frame):
    logger.info("Caught SIGINT, shutting down")
    crawler.stop()
    sys.exit(0)

if __name__ == "__main__":
    setupLogging(logging.DEBUG)
    signal.signal(signal.SIGINT, handleSigint)
    main()
    logging.shutdown()
