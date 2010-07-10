from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Host(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    last_poll = Column(DateTime)

    def __init__(self, name, address, last_poll):
        self.name = name
        self.address = address
        self.last_poll = last_poll


class Share(Base):
    __tablename__ = 'share'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    host = Column(Integer, ForeignKey('host.id'))

    def __init__(self, name, host):
        self.name = name
        self.host = host


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    share = Column(Integer, ForeignKey('share.id'))
    host = Column(Integer, ForeignKey('host.id'))

    def __init__(self, name, path, share, host):
        self.name = name
        self.path = path
        self.share = share
        self.host = host
