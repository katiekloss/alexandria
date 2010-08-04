import alexandria.exc as exc
from couchdb.http import ResourceNotFound, ResourceConflict
from couchdb.mapping import *
import couchdb
import logging

logger = logging.getLogger("alexandria.couch")

class Host(Document):
    """A generic Document representing a host"""
    name = TextField()
    age = DateTimeField()
    files = DictField()


def add_host(hostname):
    """Creates a new Host document for the given hostname"""

    hostname = hostname.lower()
    new_host = Host(name=hostname)
    new_host.id = "alexandria.host:%s" % hostname
    db = getDatabase()
    try:
        new_host.store(db)
    except ResourceConflict:
        raise exc.EditConflict("Document for host '%s' already exists"
            % hostname)


def del_host(hostname):
    """Deletes the Host document associated with the given hostname"""

    hostname = hostname.lower()
    doc_id = "alexandria.host:%s" % hostname
    db = getDatabase()
    try:
        db.delete(db[doc_id])
    except ResourceNotFound:
        raise exc.DocumentNotFound("Document for host '%s' not found"
            % hostname)


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


def store_design_doc(doc_name, views):
    """Create or update a design document with the given name and views.
    The views parameter is a nested dictionary keyed with the name of each view
    that maps to a dictionary keyed with either 'map' or 'reduce' which then
    maps to the function source:

    views['view_name']['map'] = 'map_function'
    views['view_name']['reduce'] = 'reduce_function
    """

    db = getDatabase()
    doc_full_name = "_design/%s" % doc_name

    try:
        doc = db[doc_full_name]
    except ResourceNotFound:
        db[doc_full_name] = {}
        doc = db[doc_full_name]

    doc['language'] = 'javascript'
    doc['views'] = views
    db.save(doc)
