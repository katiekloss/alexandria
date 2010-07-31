from couchdb.http import ResourceNotFound
from couchdb.mapping import *
import couchdb
import logging

logger = logging.getLogger("alexandria.couch")

class Host(Document):
    """A generic Document representing a host"""
    name = TextField()
    age = DateTimeField()
    files = ListField(TextField())


def add_host(hostname):
    """Creates a new Host document for the given hostname"""

    hostname = hostname.lower()
    new_host = Host(name=hostname)
    new_host.id = "alexandria.host:%s" % hostname
    db = getDatabase()
    new_host.store(db)


def del_host(hostname):
    """Deletes the Host document associated with the given hostname"""

    hostname = hostname.lower()
    doc_id = "alexandria.host:%s" % hostname
    db = getDatabase()
    db.delete(db[doc_id])


def getDatabaseConnection(server='127.0.0.1', port=5984):
    """Returns a couchdb.client.Server instance"""

    return couchdb.Server('http://%s:%s' % (server, port))


def getDatabase(server='127.0.0.1', port=5984, db_name='alexandria'):
    """Returns a couchdb.client.Database instance"""

    server = getDatabaseConnection(server, port)
    try:
        db = server[db_name]
        logger.debug("Opened database")
    except ResourceNotFound:
        db = server.create(db_name)
        logger.info("Created database '%s' on server" % db_name)
    return db
