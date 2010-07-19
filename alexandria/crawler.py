"""Implements the main alexandria crawler code"""

import alexandria.discover
import alexandria.couch
import threading
import logging
import time
import ConfigParser
import datetime

globalQueue = list()
globalQueueLock = threading.Lock()
pendingQueue = list()
pendingQueueLock = threading.Lock()
threadPool = []

class Crawler:
    """I'm a SMB share crawler!"""

    def __init__(self):
        self.logger = logging.getLogger("alexandria.crawler.Crawler")
        self.logger.debug("Crawler initialized")

    def run(self):
        """Runs the crawler"""

        self.logger.info("Starting")
        self.config = ConfigParser.ConfigParser()
        self.config.read('crawler.cfg')
        self.initialize_database()

        threadCount = self.config.getint('crawler', 'threads')
        for i in range(0, threadCount):
            worker = CrawlerWorker(i)
            threadPool.append(worker)
            self.logger.debug("Launching thread %s" % i)
            worker.start()
        self.logger.info("Launched thread pool with %s threads" % threadCount)

        while 1:
            self.logger.debug("Polling")
            hosts = self.get_old_hosts()
            self.logger.debug("Got %s old hosts to index" % len(hosts))
            globalQueueLock.acquire()
            pendingQueueLock.acquire()
            for row in hosts:
                if not row.key in globalQueue and not row.key in pendingQueue:
                    globalQueue.append(row.key)
                    self.logger.debug("Queued document key %s" % row.key)
            pendingQueueLock.release()
            globalQueueLock.release()
            time.sleep(60)

    def stop(self):
        self.logger.info("Shutting down")
        for worker in threadPool:
            worker.stop()
        for worker in threadPool:
            worker.join()
        self.logger.info("Stopped")

    def load_config(self):
        """Loads a config file into the Crawler"""

        self.config = ConfigParser.ConfigParser()
        self.config.read('crawler.cfg')
        self.logger.info("Loaded config file")

    def initialize_database(self):
        """Attach a CouchDB Database instance to the crawler."""

        username = self.config.get('couchdb', 'username')
        password = self.config.get('couchdb', 'password')
        self.db = alexandria.couch.getDatabase(username, password)
        self.logger.debug("Created database connection")

    def get_old_hosts(self):
        """Get a list of all hosts that need to be indexed."""

        max_age = self.config.getint('crawler', 'max_host_age')
        expire_time = datetime.datetime.now() - \
            datetime.timedelta(hours=max_age)
        expire_time = expire_time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.debug("Checking for hosts older than %s" % expire_time)
        map_fun = alexandria.couch.func_get_old_hosts % expire_time
        return list(self.db.query(map_fun))


class CrawlerWorker(threading.Thread):
    """I'm the crawler that actually writes to the database!"""

    def __init__(self, id):
        self.logger = logging.getLogger("alexandria.crawler.CrawlerWorker%s" % id)
        self.shutdown = False
        self.id = id
        threading.Thread.__init__(self)

    def run(self):
        self.logger.info("Starting")
        self.initialize_database()
        while not self.shutdown:
            self.logger.debug("Polling")
            with globalQueueLock:
                with pendingQueueLock:
                    if len(globalQueue) > 0:
                        host_key = globalQueue.pop()
                        pendingQueue.append(host_key)
                    else:
                        host_key = None
            if host_key:
                self.logger.debug("Processing key '%s'" % host_key)
                host = self.db.get(host_key)
                if 'name' in host:
                    if host['name']:
                        self.process_host(host)
                    else:
                        self.logger.warning("Document key '%s' has None as name" % host_key)
                else:
                    self.logger.warning("Document key '%s' has no name field" % host_key)
                with pendingQueueLock:
                    pendingQueue.remove(host_key)
            time.sleep(1)
        self.logger.info("Stopped")

    def stop(self):
        self.shutdown = True
        self.logger.debug("Shutting down")

    def initialize_database(self):
        """Setup a database connection to CouchDB."""
        config = ConfigParser.ConfigParser()
        config.read('crawler.cfg')
        username = config.get('couchdb', 'username')
        password = config.get('couchdb', 'password')
        self.db = alexandria.couch.getDatabase(username, password)
        self.logger.debug("Created database connection")

    def process_host(self, host):
        """Given a document for host, index that host"""
        self.logger.info("Crawling host '%s'" % host['name'])
        file_list = []
        try:
            shares = alexandria.discover.list_shares(host['name'])
            for share in shares:
                files = alexandria.discover.list_files(host['name'], share)
                file_list.append(files)
            host['files'] = file_list
        except ValueError as e:
            self.logger.error("Error while pulling filelist: %s" % e)

        host['age'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.save(host)
        self.logger.info("Crawl for host '%s' finished" % host['name'])
