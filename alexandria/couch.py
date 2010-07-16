from alexandria.config import config
from couchdb.http import ResourceNotFound
from couchdb.mapping import *
import couchdb
import logging

func_get_old_hosts = """
function(doc) {
    if(!doc.age) {
        emit(doc._id);
    } else if(doc.age < "%s") {
        emit(doc._id);
    }
}
"""

logger = logging.getLogger("alexandria.couch")

class Host(Document):
    """A generic Document representing a host"""
    name = TextField()
    age = DateTimeField()
    files = ListField(TextField())


def getDatabaseConnection(username=None, password=None,
    server='127.0.0.1', port=5984):
    """Returns a couchdb.client.Server instance"""

    return couchdb.Server('http://%s:%s@%s:%s' % (username, password, server,
        port))


def getDatabase(username=None, password=None, server='127.0.0.1', port=5984,
    db_name='alexandria'):
    """Returns a couchdb.client.Database instance"""

    server = getDatabaseConnection(username, password, server, port)
    try:
        db = server[db_name]
        logger.debug("Opened database")
    except ResourceNotFound:
        db = server.create(db_name)
        logger.info("Created database '%s' on server" % db_name)
    return db
