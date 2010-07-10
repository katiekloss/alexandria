"""Implements the main alexandria crawler code"""

import alexandria.config
import alexandria.discover
import alexandria.db
import alexandria.model
import threading
import logging

class Crawler:
    """I'm a SMB share crawler!"""

    def __init__(self):
        logging.debug("Crawler initialized")

    def run(self):
        """Runs the crawler"""
        logging.info("Crawler starting")
        alexandria.config.loadConfig('crawler.cfg')
        alexandria.db.initializeDatabase()

class CrawlerWorker():
    """I'm the crawler that actually writes to the database!"""

    def __init__(self, host):
        self.host = host

    def run(self):
        pass
