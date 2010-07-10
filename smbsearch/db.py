import smbsearch.model
from sqlalchemy import create_engine
import logging

engine = None

def getConnection():
    """Return a connection to the database"""
    pass

def initializeDatabase():
    """Prepare database connections and tables for use."""

    engine = create_engine('sqlite:///crawler.sqlite')
    logging.info("Initialized database engine")
    smbsearch.model.metadata.create_all(engine)
    logging.debug("Initialized database tables")
