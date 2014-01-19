# Fake test objects
## Peewee specific
from peewee import Model, SqliteDatabase, CharField, ForeignKeyField

peeweedb = SqliteDatabase(':memory:')

datas = [
    {'content': u'entry1'},
    {'content': u'entry2'},
    {'content': u'entry3'},
]


class BasePeeweeModel(Model):
    class Meta:
        database = peeweedb


class PeeweeSimpleDB(BasePeeweeModel):
    content = CharField()


class PeeweeDBRel(BasePeeweeModel):
    """A DB related to"""
    content = CharField()


class PeeweeDBFK(BasePeeweeModel):
    """A DB with foreign keys"""
    relate_to = ForeignKeyField(PeeweeDBRel, related_name='relaters')


def setup_peewee_db():
    PeeweeSimpleDB.create_table()
    PeeweeDBRel.create_table()
    PeeweeDBFK.create_table()

    for d in datas:
        PeeweeSimpleDB.create(**d)
        PeeweeDBRel.create(**d)
        PeeweeDBFK.create(relate_to=1)


def teardown_peewee_db():
    PeeweeSimpleDB.drop_table()
    PeeweeDBRel.drop_table()
    PeeweeDBFK.drop_table()


peeweemodel = PeeweeSimpleDB


def bottle_auth_decorator(arg):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if arg is False:
                raise Exception
            return function(*args, **kwargs)
        return wrapper
    return real_decorator

import bottle
bottleapp = bottle.Bottle

#testing with sqla
#import SQLAlchemy as sqla
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
from sqlalchemy.ext.declarative import declarative_base

#from http://flask.pocoo.org/docs/patterns/sqlalchemy/
from sqlalchemy.orm import sessionmaker, scoped_session
sqladb_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
Base = declarative_base()
#will be mandatory for api_hi .query .select_from
Base.query = sqladb_session.query_property()
Base.s = sqladb_session
# or not, we could use
# from sqlalchemy import select
# select([someModel.myColumns]).execute()

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class SQLASimpleDB(Base):
    __tablename__ = 'simplesqladb'

    id = Column(Integer, primary_key=True)
    content = Column(String)


class SQLADBRel(Base):
    __tablename__ = 'sqladbrel'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    relaters = relationship(
        "SQLADBFK",
        backref='relate_to',
        cascade="all, delete, delete-orphan")


class SQLADBFK(Base):
    __tablename__ = 'sqladbfk'

    id = Column(Integer, primary_key=True)
    relate_to_id = Column(Integer, ForeignKey("sqladbrel.id"), nullable=False)


def setup_sqla_db():
    Base.metadata.create_all(bind=engine)

    for d in datas:
        SQLASimpleDB.s.add(SQLASimpleDB(**d))
        SQLASimpleDB.s.flush()
        SQLADBRel.s.add(SQLADBRel(**d))
        SQLADBRel.s.flush()
        SQLADBFK.s.add(SQLADBFK(relate_to_id=1))
        SQLADBFK.s.flush()


def teardown_sqla_db():
    Base.metadata.drop_all(bind=engine)

sqlamodel = SQLASimpleDB


def dic_in_dic(d1, d2):
    return all(
        (k in d2 and d2[k] == v)
        for k, v in d1.iteritems())
