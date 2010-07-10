import alexandria.config
import alexandria.model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

engine = None
session = None

def getSession():
    """Return an SQLAlchemy Session instance"""

    return session()

def initializeDatabase():
    """Prepare database connections and tables for use."""

    global engine
    global session

    driver = alexandria.config.get('db', 'driver')
    db_file = alexandria.config.get('db', 'dbfile')
    engine = create_engine('%s:///%s' % (driver, db_file))
    session = sessionmaker(bind=engine)
    logging.info("Initialized database engine")

    alexandria.model.metadata.create_all(engine)
    logging.debug("Initialized database tables")
