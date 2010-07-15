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
threadPool = []

class Crawler:
    """I'm a SMB share crawler!"""

    def __init__(self):
        logging.debug("Crawler initialized")

    def run(self):
        """Runs the crawler"""

        logging.info("Crawler starting")
        self.config = ConfigParser.ConfigParser()
        self.config.read('crawler.cfg')
        self.initialize_database()

        threadCount = self.config.getint('crawler', 'threads')
        for i in range(0, threadCount):
            worker = CrawlerWorker(i)
            threadPool.append(worker)
            logging.debug("Launching thread %s" % i)
            worker.start()
        logging.info("Launched thread pool with %s threads" % threadCount)

        while 1:
            logging.debug("Crawler polling")
            hosts = self.get_old_hosts()
            logging.debug("Got %s old hosts to index" % len(hosts))
            globalQueueLock.acquire()
            for row in hosts:
                if not row.key in globalQueue:
                    globalQueue.append(row.key)
            logging.debug("Queue size: %s" % len(globalQueue))
            globalQueueLock.release()
            time.sleep(60)

    def stop(self):
        logging.info("Shutting down thread pool")
        for worker in threadPool:
            worker.stop()
        for worker in threadPool:
            worker.join()
        logging.info("Crawler stopped")

    def load_config(self):
        """Loads a config file into the Crawler"""

        self.config = ConfigParser.ConfigParser()
        self.config.read('crawler.cfg')
        logging.info("Loaded config file")

    def initialize_database(self):
        """Attach a CouchDB Database instance to the crawler."""

        username = self.config.get('couchdb', 'username')
        password = self.config.get('couchdb', 'password')
        self.db = alexandria.couch.getDatabase(username, password)

    def get_old_hosts(self):
        """Get a list of all hosts that need to be indexed."""

        max_age = self.config.getint('crawler', 'max_host_age')
        expire_time = datetime.datetime.now() - \
            datetime.timedelta(hours=max_age)
        expire_time = expire_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.debug("Checking for hosts older than %s" % expire_time)
        map_fun = alexandria.couch.func_get_old_hosts % expire_time
        return list(self.db.query(map_fun))


class CrawlerWorker(threading.Thread):
    """I'm the crawler that actually writes to the database!"""

    def __init__(self, id):
        self.shutdown = False
        self.id = id
        threading.Thread.__init__(self)

    def run(self):
        self.initialize_database()
        while not self.shutdown:
            logging.debug("Worker %s polling" % self.id)
            globalQueueLock.acquire()
            if len(globalQueue) > 0:
                host_key = globalQueue.pop()
            else:
                host_key = None
            globalQueueLock.release()
            if host_key:
                logging.debug("Worker %s processing key '%s'" % (self.id, host_key))
                host = self.db.get(host_key)

                if not host:        # This shouldn't happen
                    logging.error("Worker %s failed to find document key '%s'" % (self.id, host_key))
                    return

                file_list = []
                try:
                    shares = alexandria.discover.list_shares(host['name'])
                    for share in shares:
                        files = alexandria.discover.list_files(host['name'], share)
                        file_list.append(files)
                    host['files'] = file_list
                except ValueError, e:
                    logging.error("Worker %s got error: %s" % (self.id, e.value))

                host['age'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.db.save(host)
                logging.info("Worker %s: crawl for host '%s' finished" % (self.id, host['name']))
            time.sleep(45)
        logging.info("Worker %s stopping" % self.id)

    def stop(self):
        self.shutdown = True
        logging.debug("Worker %s set to shutdown" % self.id)

    def initialize_database(self):
        """Setup a database connection to CouchDB."""
        config = ConfigParser.ConfigParser()
        config.read('crawler.cfg')
        username = config.get('couchdb', 'username')
        password = config.get('couchdb', 'password')
        self.db = alexandria.couch.getDatabase(username, password)
