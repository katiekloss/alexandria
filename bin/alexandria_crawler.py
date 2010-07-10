#!/usr/bin/env python

import os
import sys

try:
    import alexandria
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import alexandria

import logging
import alexandria.discover
import alexandria.crawler

def setupLogging(log_level):
    """Initializes the Python logging module."""
    logging.basicConfig(filename="crawler.log", level=log_level,
        format='%(asctime)s - %(module)s:%(funcName)s(%(lineno)d):%(levelname)s - %(message)s')

def main():
    """Run a crawler"""
    crawler = alexandria.crawler.Crawler()
    crawler.run()

if __name__ == "__main__":
    setupLogging(logging.DEBUG)
    main()
