import unittest as u
from api_hi.helpers import PeeweeHelper

from peewee import Model, SqliteDatabase, CharField, ForeignKeyField

database = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = database


class SimpleDB(BaseModel):
    content = CharField()


class DBRel(BaseModel):
    """A DB related to"""
    content = CharField()


class DBFK(BaseModel):
    """A DB with foreign keys"""
    relate_to = ForeignKeyField(DBRel, related_name='relaters')


def setup_db():
    SimpleDB.create_table()
    DBRel.create_table()
    DBFK.create_table()

    datas = [
        {'content': u'entry1'},
        {'content': u'entry2'},
        {'content': u'entry3'},
    ]

    for d in datas:
        SimpleDB.create(**d)
        DBRel.create(**d)
        DBFK.create(relate_to=1)


def teardown_db():
    SimpleDB.drop_table()
    DBRel.drop_table()
    DBFK.drop_table()
    

model = SimpleDB


class TestPeeweeHelper(u.TestCase):
    """Feature: we got helpers to do simple sqla queries"""
    def setUp(self):
        setup_db()
        self.simple = PeeweeHelper(SimpleDB)
        self.fk = PeeweeHelper(DBFK)
        self.rel = PeeweeHelper(DBRel)

    def tearDown(self):
        teardown_db()

    def test_get_columns(self):
        """Scenario: get the columns of the model"""
        rel_cols = set([DBRel.relaters, DBRel.content, DBRel.id])
        self.assertEquals(rel_cols, self.rel.columns())

    def test_get_filtered_columns(self):
        """Scenario: get the filtered columns of the model"""
        rel_cols = set([DBRel.relaters, DBRel.id])
        self.assertEquals(rel_cols, self.rel.columns(['relaters', 'id']))

    def test_get_relations(self):
        """Get relations from an entry"""
        entry = DBRel.select().first()
        rels = {'relaters': [x.id for x in entry.relaters]}
        result = self.rel.get_relations(entry)
        self.assertEquals(rels, result)

    def test_get_filtered_relations(self):
        """Get relations from an entry"""
        entry = DBRel.select(DBRel.id).first()
        rels = {}
        result = self.rel.get_relations(entry, ['id'])
        self.assertEquals(rels, result)

    def test_select(self):
        """Scenario: we get a list of simple entries
        ie: table with one primary key, and no references"""
        entries = DBRel.select()
        result = self.rel.select()
        self.assertEquals(entries, result)

    def test_where(self):
        """We want specific ID details"""
        entries = DBRel.select()
        entry = entries.first()._data
        entry['relaters'] = [1, 2, 3]
        result = self.rel.where(entries, 1)
        self.assertEquals(entry, result['result'])

    def test_all(self):
        """We want all the entries"""
        entries = DBRel.select()
        entry = list(entries.dicts())
        first = entry[0]
        first['relaters'] = [1, 2, 3]
        second = entry[1]
        second['relaters'] = []
        result = self.rel.all(entries)
        self.assertEquals(first, result['result'][0])
        self.assertEquals(second, result['result'][1])

    def test_add(self):
        """We add an entry"""
        entry = {'content': u'entry4'}
        result = self.rel.add(**entry)
        exp = entry
        exp['id'] = 4
        self.assertEquals(exp, result)

    def test_update(self):
        """We update an entry"""
        entry = {'content': u'entry4'}
        result = self.rel.update(1, **entry)
        exp = entry
        exp['id'] = 1
        self.assertEquals(exp, result)

    def test_delete(self):
        """We delete an entry"""
        self.rel.delete(1)
        entries = self.rel.model.select()
        self.assertEquals(None, self.rel.where(entries, 1)['result'])

from api_hi.helpers import BottleHelper
from bottle import Bottle

app = Bottle()


class TestBottleHelper(u.TestCase):
    """Test bottlepy helper"""
    def setUp(self):
        self.helper = BottleHelper(app)

    def test_route(self):
        """Scenario: we add a route"""
        self.assertEquals(app.routes, self.helper.app.routes)
        self.helper.route('/test', lambda: True, ['GET', 'POST'])
        self.assertEquals(app.routes, self.helper.app.routes)

    def test_get_request_datas(self):
        """Scenario: we need to get some data from the request
        """
        self.assertIsNone(
            self.helper.request('test'))
        self.assertIsNone(
            self.helper.request(['test']))

# #testing with sqla
# #import SQLAlchemy as sqla
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///:memory:', echo=True)
# from sqlalchemy.ext.declarative import declarative_base

# #from http://flask.pocoo.org/docs/patterns/sqlalchemy/
# from sqlalchemy.orm import sessionmaker, scoped_session
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# #will be mandatory for api_hi .query .select_from
# Base.query = db_session.query_property()
# Base.s = db_session
# # or not, we could use
# # from sqlalchemy import select
# # select([someModel.myColumns]).execute()

# from sqlalchemy import Column, Integer, String, ForeignKey
# #from sqlalchemy.orm import relationship


# class SimpleSqlaDB(Base):
#     __tablename__ = 'simplesqladb'

#     id = Column(Integer, primary_key=True)
#     content = Column(String)


# class SqlaDBRel(Base):
#     __tablename__ = 'sqladbrel'

#     id = Column(Integer, primary_key=True)
#     content = Column(String)


# class SqlaDBFK(Base):
#     __tablename__ = 'sqladbfk'

#     id = Column(Integer, primary_key=True)
#     relate_to = Column(Integer, ForeignKey("sqladbrel.id"), nullable=False)
#     #relate_to = relationship("SqlaDBRel", backref='relaters')

# Base.metadata.create_all(bind=engine)

# datas = [
#     {'content': u'entry1'},
#     {'content': u'entry2'},
#     {'content': u'entry3'},
# ]

# for d in datas:
#     SimpleSqlaDB.s.add(SimpleSqlaDB(**d))
#     SqlaDBRel.s.add(SqlaDBRel(**d))
#     SqlaDBFK.s.add(SqlaDBFK(relate_to=1))

# model = SimpleDB


# TestAPISQLA = type('MapBasicAPIToSQLAModel',
#                    (MapBasicAPIToModel,), dict(
#                        simpledb=SimpleSqlaDB,
#                        dbrel=SqlaDBRel,
#                        dbfk=SqlaDBFK))
