"""Implements the main smbsearch crawler code"""

import smbsearch.config
import smbsearch.discover
import smbsearch.db
import smbsearch.model
import threading
import logging

class Crawler:
    """I'm a SMB share crawler!"""

    def __init__(self):
        logging.debug("Crawler initialized")

    def run(self):
        """Runs the crawler"""
        logging.info("Crawler starting")
        smbsearch.config.loadConfig('crawler.cfg')
        smbsearch.db.initializeDatabase()

class CrawlerWorker():
    """I'm the crawler that actually writes to the database!"""

    def __init__(self, host):
        self.host = host

    def run(self):
        pass
