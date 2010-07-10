import smbsearch.config
import smbsearch.model
from sqlalchemy import create_engine
import logging

engine = None

def getConnection():
    """Return a connection to the database"""
    pass

def initializeDatabase():
    """Prepare database connections and tables for use."""

    driver = smbsearch.config.get('db', 'driver')
    db_file = smbsearch.config.get('db', 'dbfile')
    engine = create_engine('%s:///%s' % (driver, db_file))
    logging.info("Initialized database engine")
    smbsearch.model.metadata.create_all(engine)
    logging.debug("Initialized database tables")
